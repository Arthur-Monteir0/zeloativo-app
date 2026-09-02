import asyncio
from dataclasses import dataclass
from datetime import datetime, date, timedelta
import math
import sys
import time

import flet as ft
from services.data_service import DataService

_HAS_WINSOUND = False
if sys.platform.startswith("win"):
    try:
        import winsound  # type: ignore
        _HAS_WINSOUND = True
    except Exception:
        _HAS_WINSOUND = False


@dataclass
class AlarmConfig:
    minutes_before: int = 5
    check_interval_sec: int = 20
    allow_late_alert: bool = True

    # 🔔 comportamento do alarme
    sound_enabled: bool = True
    beep_freq: int = 1200
    beep_duration_ms: int = 300
    beep_interval_sec: float = 1.2   # intervalo entre bipes
    max_beep_seconds: int = 120      # 2 minutos

    snooze_minutes: int = 15         # tempo do "Adiei"


class AlarmService:
    """
    - Quando estiver perto da próxima dose PENDING:
      abre um popup com botões "Tomei" e "Adiei"
      e apita por até 2 minutos até o usuário clicar.
    """

    def __init__(self, page: ft.Page, config: AlarmConfig | None = None):
        self.page = page
        self.config = config or AlarmConfig()
        self._running = False

        self._active_alarm = False
        self._stop_beep = asyncio.Event()

        self._last_event_id_alerted: str | None = None
        self._snoozed_until: dict[str, datetime] = {}  # event_id -> datetime

    def start(self):
        if self._running:
            return
        self._running = True
        self.page.run_task(self._loop)

    def stop(self):
        self._running = False
        self._active_alarm = False
        self._last_event_id_alerted = None
        self._snoozed_until.clear()
        try:
            self._stop_beep.set()
        except Exception:
            pass

    # ------------------- som -------------------
    async def _beep_loop(self):
        if not self.config.sound_enabled or not _HAS_WINSOUND:
            return

        self._stop_beep.clear()
        end_ts = time.time() + self.config.max_beep_seconds

        while time.time() < end_ts and not self._stop_beep.is_set():
            try:
                winsound.Beep(int(self.config.beep_freq), int(self.config.beep_duration_ms))
            except Exception:
                break
            await asyncio.sleep(self.config.beep_interval_sec)

    # ------------------- util -------------------
    def _find_next_pending(self, items: list[dict]):
        now = datetime.now()
        today_iso = date.today().isoformat()

        candidates: list[tuple[datetime, dict]] = []
        for ev in items:
            if ev.get("status") != "pending":
                continue

            ev_id = ev.get("id")
            if ev_id and ev_id in self._snoozed_until:
                if now < self._snoozed_until[ev_id]:
                    continue  # ainda está “adiado” no app

            hhmm = ev.get("time")
            if not hhmm:
                continue

            try:
                h, m = hhmm.split(":")
                dt = datetime.fromisoformat(today_iso).replace(
                    hour=int(h), minute=int(m), second=0, microsecond=0
                )
                candidates.append((dt, ev))
            except Exception:
                continue

        if not candidates:
            return None, None

        candidates.sort(key=lambda x: x[0])

        for dt, ev in candidates:
            diff_sec = (dt - now).total_seconds()

            if diff_sec >= 0:
                minutes_left = int(math.ceil(diff_sec / 60))
                return ev, minutes_left

            minutes_left = int(math.floor(diff_sec / 60))
            if self.config.allow_late_alert and diff_sec >= -(self.config.minutes_before * 60):
                return ev, minutes_left

        return None, None

    def _snack(self, msg: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
        self.page.update()

    # ------------------- popup + ações -------------------
    def _show_alarm_dialog(self, ev: dict, minutes_left: int):
        ev_id = ev.get("id")
        nome = ev.get("medicine_name", "Remédio")
        hora = ev.get("time", "--:--")

        if minutes_left >= 0:
            title = "Hora do remédio"
            body = f"Falta {minutes_left} min: {nome} às {hora}"
        else:
            title = "Remédio atrasado"
            body = f"{nome} era às {hora}"

        dialog = None

        def close_dialog():
            nonlocal dialog
            if dialog:
                dialog.open = False
                self.page.update()

        def tomei(e=None):
            # para o som
            self._stop_beep.set()
            self._active_alarm = False
            close_dialog()

            # atualiza no backend (marcar como tomado)
            if ev_id:
                try:
                    DataService.update_intake_status(ev_id, "taken")
                except Exception:
                    pass

            self._snack("✅ Marcado como: Tomei")

        def adiei(e=None):
            # para o som
            self._stop_beep.set()
            self._active_alarm = False
            close_dialog()

            # ✅ snooze real no backend (+15 min)
            if ev_id:
                try:
                    DataService.snooze_intake(ev_id, 15)
                except Exception:
                    pass

            self._snack("⏱️ Adiado por 15 min")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Text(body),
            actions=[
                ft.ElevatedButton("Adiei", on_click=adiei),
                ft.ElevatedButton("Tomei", on_click=tomei),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        # overlay é o jeito mais compatível
        if dialog not in self.page.overlay:
            self.page.overlay.append(dialog)

        dialog.open = True
        self.page.update()

    async def _trigger_alarm(self, ev: dict, minutes_left: int):
        # evita abrir dois alarmes ao mesmo tempo
        if self._active_alarm:
            return

        self._active_alarm = True
        self._stop_beep.clear()

        # abre popup
        self._show_alarm_dialog(ev, minutes_left)

        # começa o som (até 2 min ou até clicar Tomei/Adiei)
        await self._beep_loop()

        # se chegou aqui sem clicar, encerra estado ativo (para poder alertar de novo depois)
        self._active_alarm = False

    # ------------------- loop principal -------------------
    async def _loop(self):
        while self._running:
            try:
                if not DataService.token:
                    await asyncio.sleep(self.config.check_interval_sec)
                    continue

                hoje = date.today().isoformat()
                data = DataService.get_day_history(hoje)
                items = data.get("items", []) if isinstance(data, dict) else []

                ev, minutes_left = self._find_next_pending(items)

                if ev and minutes_left is not None:
                    ev_id = ev.get("id")

                    # condição de disparo
                    if minutes_left <= self.config.minutes_before:
                        # evita repetir em loop pro mesmo evento
                        if ev_id and ev_id == self._last_event_id_alerted and self._active_alarm:
                            await asyncio.sleep(self.config.check_interval_sec)
                            continue

                        self._last_event_id_alerted = ev_id
                        await self._trigger_alarm(ev, minutes_left)

            except Exception:
                pass

            await asyncio.sleep(self.config.check_interval_sec)