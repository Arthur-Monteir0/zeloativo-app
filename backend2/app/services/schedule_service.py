from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date, time, timedelta, timezone
from typing import List, Optional


@dataclass
class IntakeToCreate:
    scheduled_at: str  # ISO string
    status: str = "pending"


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return date.fromisoformat(s)


def _parse_time(s: Optional[str]) -> Optional[time]:
    if not s:
        return None
    # aceita "08:00" ou "08:00:00"
    return time.fromisoformat(s)


def generate_intakes(
    start_date: str,
    start_time: str,
    end_date: str,
    interval_hours: int,
    tz_offset_hours: int = -3,  # Brasil (Belém é -03:00)
    max_events: int = 2000,
) -> List[IntakeToCreate]:
    """
    Gera lista de doses (scheduled_at) de start até end, pulando interval_hours.
    scheduled_at é gerado como ISO com timezone (ex: 2026-03-04T08:00:00-03:00).
    """
    sd = _parse_date(start_date)
    st = _parse_time(start_time)
    ed = _parse_date(end_date)

    if not sd or not st or not ed:
        raise ValueError("start_date, start_time e end_date são obrigatórios")

    if interval_hours < 1:
        raise ValueError("interval_hours precisa ser >= 1")

    tz = timezone(timedelta(hours=tz_offset_hours))
    start_dt = datetime.combine(sd, st).replace(tzinfo=tz)

    # regra: fim no final do dia de end_date
    end_dt = datetime.combine(ed, time(23, 59, 59)).replace(tzinfo=tz)

    if start_dt > end_dt:
        raise ValueError("Data/hora inicial não pode ser maior que a final")

    step = timedelta(hours=interval_hours)

    out: List[IntakeToCreate] = []
    cur = start_dt
    while cur <= end_dt:
        out.append(IntakeToCreate(scheduled_at=cur.isoformat(), status="pending"))
        if len(out) > max_events:
            raise ValueError("Muitas doses geradas. Reduza o período ou aumente o intervalo.")
        cur = cur + step

    return out