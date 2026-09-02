from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import random

from app.database import supabase
from app.routes.history_routes import get_user_id_from_token  # pode manter assim por enquanto

router = APIRouter(prefix="/link", tags=["link"])


def gen_code(n: int = 6) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(random.choice(alphabet) for _ in range(n))


class AcceptIn(BaseModel):
    code: str


@router.post("/code")
def generate_link_code(authorization: str | None = Header(default=None)):
    user_id = get_user_id_from_token(authorization)

    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    # tenta até 10 vezes pra evitar colisão se tiver unique(code)
    for _ in range(10):
        code = gen_code(6)

        payload = {
            "owner_user_id": user_id,
            "code": code,
            "expires_at": expires_at.isoformat(),
            "used_at": None,
            # ⚠️ AJUSTE AQUI se sua coluna for "used_by" em vez de "used_by_user_id"
            "used_by": None,
        }

        try:
            res = supabase.table("link_codes").insert(payload).execute()
            if res.data:
                return {"code": code, "expires_at": expires_at.isoformat()}
        except Exception as e:
            msg = str(e).lower()
            if "duplicate" in msg or "unique" in msg:
                continue
            raise HTTPException(status_code=500, detail=f"Erro ao salvar link_code: {e}")

    raise HTTPException(status_code=500, detail="Não foi possível gerar um código único")


@router.post("/accept")
def accept_link_code(payload: AcceptIn, authorization: str | None = Header(default=None)):
    caregiver_id = get_user_id_from_token(authorization)

    code = (payload.code or "").strip().upper()
    if not code:
        raise HTTPException(status_code=400, detail="Código vazio")

    rows = (
        supabase.table("link_codes")
        .select("*")
        .eq("code", code)
        .is_("used_at", None)
        .execute()
    ).data or []

    if not rows:
        raise HTTPException(status_code=400, detail="Código inválido ou já usado")

    link = rows[0]

    expires_at = link.get("expires_at")
    if not expires_at:
        raise HTTPException(status_code=400, detail="Código inválido")

    exp = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Código expirado")

    patient_id = link["owner_user_id"]

    if patient_id == caregiver_id:
        raise HTTPException(status_code=400, detail="Você não pode vincular com você mesmo")

    # evita vínculo duplicado
    exists = (
        supabase.table("care_links")
        .select("id")
        .eq("patient_user_id", patient_id)
        .eq("caregiver_user_id", caregiver_id)
        .execute()
    ).data or []

    if exists:
        raise HTTPException(status_code=400, detail="Esse vínculo já existe")

    # cria vínculo
    supabase.table("care_links").insert({
        "patient_user_id": patient_id,
        "caregiver_user_id": caregiver_id,
    }).execute()

    # marca código como usado
    supabase.table("link_codes").update({
        "used_at": datetime.now(timezone.utc).isoformat(),
        # ⚠️ AJUSTE AQUI se sua coluna for "used_by" em vez de "used_by_user_id"
        "used_by": caregiver_id,
    }).eq("id", link["id"]).execute()

    return {"ok": True, "patient_user_id": patient_id}


@router.get("/my-links")
def my_links(authorization: str | None = Header(default=None)):
    user_id = get_user_id_from_token(authorization)

    patients = (
        supabase.table("care_links")
        .select("patient_user_id, created_at")
        .eq("caregiver_user_id", user_id)
        .execute()
    ).data or []

    caregivers = (
        supabase.table("care_links")
        .select("caregiver_user_id, created_at")
        .eq("patient_user_id", user_id)
        .execute()
    ).data or []

    return {"patients": patients, "caregivers": caregivers}
from fastapi import Query

@router.delete("/unlink")
def unlink(
    patient_user_id: str = Query(..., description="uuid do paciente que será desvinculado"),
    authorization: str | None = Header(default=None),
):
    caregiver_id = get_user_id_from_token(authorization)

    # apaga o vínculo (caregiver -> patient)
    res = (
        supabase.table("care_links")
        .delete()
        .eq("patient_user_id", patient_user_id)
        .eq("caregiver_user_id", caregiver_id)
        .execute()
    )

    return {"ok": True, "deleted": bool(res.data)}