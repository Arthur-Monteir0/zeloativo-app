from fastapi import APIRouter, HTTPException, Header, Query
from datetime import date, datetime, timedelta, timezone
import os
import jwt
from dotenv import load_dotenv
from pydantic import BaseModel

from app.database import supabase, supabase_for_user  # ✅ agora usamos os dois

load_dotenv()

router = APIRouter(prefix="/history", tags=["history"])
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # opcional


def _extract_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    return parts[1]


def get_user_id_from_token(authorization: str | None) -> str:
    token = _extract_token(authorization)

    if JWT_SECRET:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id

    # fallback: supabase get_user
    try:
        u = supabase.auth.get_user(token)
        user = getattr(u, "user", None) or (u.get("user") if isinstance(u, dict) else None)
        if user and getattr(user, "id", None):
            return user.id
    except Exception:
        pass

    raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/day")
def history_day(
    day: str = Query(..., description="YYYY-MM-DD"),
    patient_id: str | None = Query(default=None, description="uuid do paciente (opcional)"),
    tz_offset_hours: int = Query(default=-3, description="Fuso do usuário (ex: -3 Brasil)"),
    authorization: str | None = Header(default=None),
):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)  # ✅ RLS ok

    target_id = user_id

    # valida vínculo (também com sb)
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

    # dia LOCAL -> intervalo UTC
    tz = timezone(timedelta(hours=tz_offset_hours))
    local_start = datetime.fromisoformat(day).replace(tzinfo=tz)
    local_end = local_start + timedelta(days=1) - timedelta(seconds=1)

    start_utc = local_start.astimezone(timezone.utc).isoformat()
    end_utc = local_end.astimezone(timezone.utc).isoformat()

    sb_query = sb if target_id == user_id else supabase  # ✅ cuidador lê paciente via service role

    events = (
        sb_query.table("intake_events")
        .select("id, medicine_id, scheduled_at, status, taken_at, notes, medicines(name)")
        .eq("user_id", target_id)
        .gte("scheduled_at", start_utc)
        .lte("scheduled_at", end_utc)
        .order("scheduled_at", desc=False)
        .execute()
    ).data or []

    items = []
    taken = 0
    total = 0

    for ev in events:
        total += 1
        status = ev.get("status") or "pending"
        if status == "taken":
            taken += 1

        med_name = None
        med_rel = ev.get("medicines")
        if isinstance(med_rel, dict):
            med_name = med_rel.get("name")
        elif isinstance(med_rel, list) and len(med_rel) > 0:
            med_name = med_rel[0].get("name")

        sched = ev.get("scheduled_at")
        try:
            dt_utc = datetime.fromisoformat(str(sched).replace("Z", "+00:00"))
            dt_local = dt_utc.astimezone(tz)
            time_str = dt_local.strftime("%H:%M")
        except Exception:
            time_str = "--:--"

        items.append(
            {
                "id": ev.get("id"),
                "medicine_id": ev.get("medicine_id"),
                "medicine_name": med_name or "Remédio",
                "time": time_str,
                "scheduled_at": sched,
                "status": status,
            }
        )

    adherence = int(round((taken / total) * 100)) if total > 0 else 0
    return {"date": day, "adherence_percent": adherence, "items": items}


@router.get("/weekly")
def history_weekly(
    patient_id: str | None = Query(default=None, description="uuid do paciente (opcional)"),
    tz_offset_hours: int = Query(default=-3, description="Fuso do usuário (ex: -3 Brasil)"),
    authorization: str | None = Header(default=None),
):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)  # ✅ RLS ok

    target_id = user_id

    # valida vínculo
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

    today = date.today()
    start = today - timedelta(days=6)

    weekly_data = []
    dates = []
    days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    tz = timezone(timedelta(hours=tz_offset_hours))

    sb_query = sb if target_id == user_id else supabase  # ✅ cuidador lê paciente via service role

    for i in range(7):
        d = start + timedelta(days=i)
        iso = d.isoformat()
        dates.append(str(d.day))

        local_start = datetime.fromisoformat(iso).replace(tzinfo=tz)
        local_end = local_start + timedelta(days=1) - timedelta(seconds=1)
        start_utc = local_start.astimezone(timezone.utc).isoformat()
        end_utc = local_end.astimezone(timezone.utc).isoformat()

        evs = (
            sb_query.table("intake_events")
            .select("status")
            .eq("user_id", target_id)
            .gte("scheduled_at", start_utc)
            .lte("scheduled_at", end_utc)
            .execute()
        ).data or []

        total = len(evs)
        taken = sum(1 for x in evs if (x.get("status") or "pending") == "taken")
        adherence = int(round((taken / total) * 100)) if total > 0 else 0
        weekly_data.append(adherence)

    average = int(round(sum(weekly_data) / 7)) if weekly_data else 0

    start_wd = start.weekday()  # Monday=0
    ordered_days = [days[(start_wd + i) % 7] for i in range(7)]

    return {
        "start_date": start.isoformat(),
        "days": ordered_days,
        "dates": dates,
        "weekly_data": weekly_data,
        "average": average,
    }


class IntakeUpdate(BaseModel):
    status: str  # "taken" | "missed" | "pending"


@router.patch("/intakes/{event_id}")
def update_intake(event_id: str, payload: IntakeUpdate, authorization: str | None = Header(default=None)):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)  # ✅ RLS ok

    status = payload.status
    if status not in ("taken", "missed", "pending"):
        raise HTTPException(status_code=400, detail="status must be taken, missed or pending")

    update_data = {"status": status}

    if status == "taken":
        update_data["taken_at"] = datetime.now(timezone.utc).isoformat()
    else:
        update_data["taken_at"] = None

    res = (
        sb.table("intake_events")
        .update(update_data)
        .eq("id", event_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not res.data:
        raise HTTPException(status_code=404, detail="Intake event not found")

    return res.data[0]

