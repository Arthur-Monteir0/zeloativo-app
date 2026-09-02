from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

from app.database import supabase_for_user
from app.routes.history_routes import get_user_id_from_token, _extract_token  # reaproveita

router = APIRouter(prefix="/intakes", tags=["intakes"])


class IntakeUpdate(BaseModel):
    status: str  # "taken" | "missed" | "pending"


@router.patch("/{event_id}")
def update_intake_status(
    event_id: str,
    payload: IntakeUpdate,
    authorization: str | None = Header(default=None),
):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)

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


@router.patch("/{event_id}/snooze")
def snooze_intake(
    event_id: str,
    minutes: int = Query(default=15, ge=1, le=180),
    authorization: str | None = Header(default=None),
):
    user_id = get_user_id_from_token(authorization)
    token = _extract_token(authorization)
    sb = supabase_for_user(token)

    # pega evento do usuário
    res = (
        sb.table("intake_events")
        .select("id, user_id, status, scheduled_at")
        .eq("id", event_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    ev = res.data
    if not ev:
        raise HTTPException(status_code=404, detail="Intake event not found")

    if (ev.get("status") or "pending") != "pending":
        raise HTTPException(status_code=400, detail="Só é possível adiar eventos pendentes")

    sched = ev.get("scheduled_at")
    if not sched:
        raise HTTPException(status_code=400, detail="Evento sem scheduled_at")

    try:
        dt = datetime.fromisoformat(str(sched).replace("Z", "+00:00"))
    except Exception:
        raise HTTPException(status_code=400, detail="scheduled_at inválido")

    new_dt = dt + timedelta(minutes=minutes)

    upd = (
        sb.table("intake_events")
        .update({"scheduled_at": new_dt.isoformat()})
        .eq("id", event_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not upd.data:
        raise HTTPException(status_code=500, detail="Falha ao atualizar scheduled_at")

    return {"detail": f"Adiado em {minutes} minutos", "event": upd.data[0]}