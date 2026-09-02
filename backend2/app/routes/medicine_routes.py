from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel, Field
from typing import Optional
from app.services.schedule_service import generate_intakes
import jwt
import os
from dotenv import load_dotenv

from app.database import supabase  # mantém para auth.get_user() fallback
from app.database import supabase_for_user

load_dotenv()

router = APIRouter(prefix="/medicines", tags=["medicines"])
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # opcional (recomendado)


def _extract_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    return parts[1]


def get_user_id_from_token(authorization: str | None) -> str:
    token = _extract_token(authorization)

    # Se tiver JWT secret do Supabase, decodifica local
    if JWT_SECRET:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id

    # fallback: tenta pelo supabase get_user
    try:
        u = supabase.auth.get_user(token)
        user = getattr(u, "user", None) or (u.get("user") if isinstance(u, dict) else None)
        if user and getattr(user, "id", None):
            return user.id
    except Exception:
        pass

    raise HTTPException(status_code=401, detail="Invalid token")


class MedicineIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    dosage: Optional[str] = None
    notes: Optional[str] = None
    interval_hours: int = Field(default=8, ge=1, le=72)
    start_date: Optional[str] = None
    start_time: Optional[str] = None
    end_date: Optional[str] = None
    image_url: Optional[str] = None


@router.get("")
def list_medicines(
    authorization: str | None = Header(default=None),
    patient_id: str | None = Query(default=None, description="uuid do paciente (opcional)"),
):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)

    target_id = user_id

    # se veio patient_id (cuidador querendo ver paciente), valida vínculo
    # (care_links também pode ter RLS; se tiver, troque supabase -> sb aqui)
    if patient_id and patient_id != user_id:
        link = (
            sb.table("care_links")
            .select("id")
            .eq("patient_user_id", patient_id)
            .eq("caregiver_user_id", user_id)
            .execute()
        ).data or []

        if not link:
            raise HTTPException(status_code=403, detail="Sem permissão para ver esse paciente")

        target_id = patient_id

    res = (
        sb.table("medicines")
        .select("*")
        .eq("user_id", target_id)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


@router.post("")
def create_medicine(payload: MedicineIn, authorization: str | None = Header(default=None)):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)

    data = payload.model_dump()
    data["user_id"] = user_id

    res = sb.table("medicines").insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Insert failed")

    med = res.data[0]

    # ✅ GERAR DOSES AUTOMATICAMENTE
    try:
        if med.get("start_date") and med.get("start_time") and med.get("end_date"):
            doses = generate_intakes(
                start_date=med["start_date"],
                start_time=med["start_time"],
                end_date=med["end_date"],
                interval_hours=int(med.get("interval_hours") or 8),
                tz_offset_hours=-3,
            )

            intake_rows = [
                {
                    "user_id": user_id,
                    "medicine_id": med["id"],
                    "scheduled_at": d.scheduled_at,
                    "status": d.status,
                }
                for d in doses
            ]

            chunk_size = 500
            for i in range(0, len(intake_rows), chunk_size):
                resp = sb.table("intake_events").insert(intake_rows[i:i + chunk_size]).execute()
                if not resp.data:
                    raise Exception("Falha ao inserir intake_events (RLS/policy?)")

    except Exception as e:
        med["schedule_warning"] = str(e)

    return med


@router.patch("/{medicine_id}")
def update_medicine(medicine_id: str, payload: MedicineIn, authorization: str | None = Header(default=None)):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)

    data = payload.model_dump()

    res = (
        sb.table("medicines")
        .update(data)
        .eq("id", medicine_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return res.data[0]


@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: str, authorization: str | None = Header(default=None)):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)

    res = (
        sb.table("medicines")
        .delete()
        .eq("id", medicine_id)
        .eq("user_id", user_id)
        .execute()
    )
    return {"deleted": bool(res.data)}