import flet as ft
from fastapi import Query
from datetime import date, timedelta,timezone
from utils.theme import AppColors
from services.data_service import DataService


def history_view(page: ft.Page, patient_id: str | None = None):
    page.bgcolor = "#FFFFFF"

    # ---------------- Estado ----------------
    state = {
        "weekly_data": [0, 0, 0, 0, 0, 0, 0],  # percentuais
        "days": ["", "", "", "", "", "", ""],  # "SEG", "TER"...
        "dates": ["", "", "", "", "", "", ""],  # "1", "2"...
        "iso_days": ["", "", "", "", "", "", ""],  # YYYY-MM-DD
        "average": 0,
        "selected_index": 6,
        "day_items": [],  # lista do /history/day
        "day_percent": 0,
    }

    # Container principal que será re-renderizado
    history_container = ft.Container(expand=True, bgcolor="#FFFFFF", padding=20)

    def show_error(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
        page.update()

    # ---------------- UI helpers ----------------
    def average_color(avg: int) -> str:
        return "green" if avg >= 60 else "red"

    def status_ui(status: str):
        status = (status or "pending").lower()
        if status == "taken":
            return ft.Icons.CHECK_CIRCLE, "green", "Tomado"
        if status == "missed":
            return ft.Icons.CANCEL, "red", "Perdido"
        return ft.Icons.ACCESS_TIME, "orange", "Pendente"

    def med_item(name: str, time_str: str, status: str):
        icon, color, label = status_ui(status)
        return ft.Container(
            padding=15,
            border_radius=12,
            bgcolor="#F5F7FA",
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=color, size=28),
                    ft.Column(
                        spacing=2,
                        expand=True,
                        controls=[
                            ft.Text(name, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),
                            ft.Text(time_str, size=12, color=AppColors.SECONDARY),
                        ],
                    ),
                    ft.Text(label, color=color, weight=ft.FontWeight.BOLD),
                ]
            ),
        )

    def build_chart(weekly_data):
        # barras com altura proporcional (min 12)
        bars = []
        for value in weekly_data:
            v = max(0, min(100, int(value or 0)))
            bars.append(
                ft.Container(
                    width=22,
                    height=12 + int(v * 1.3),
                    bgcolor=AppColors.PRIMARY,
                    border_radius=6,
                )
            )

        return ft.Container(
            height=180,
            content=ft.Row(
                bars,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
        )

    def build_day_selector():
        buttons = []

        for i in range(7):
            is_selected = i == state["selected_index"]

            buttons.append(
                ft.Container(
                    padding=10,
                    border_radius=20,
                    bgcolor=AppColors.SECONDARY if is_selected else "#F2F2F2",
                    on_click=lambda e, idx=i: change_day(idx),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                        controls=[
                            ft.Text(
                                state["dates"][i] if i < len(state["dates"]) else "",
                                weight=ft.FontWeight.BOLD,
                                color="white" if is_selected else AppColors.SECONDARY,
                            ),
                            ft.Text(
                                state["days"][i] if i < len(state["days"]) else "",
                                size=10,
                                color="white" if is_selected else AppColors.SECONDARY,
                            ),
                        ],
                    ),
                )
            )

        return ft.Row(buttons, alignment=ft.MainAxisAlignment.SPACE_AROUND)

    # ---------------- Data loaders ----------------
    def load_day_by_index(idx: int):
        iso = state["iso_days"][idx] if idx < len(state["iso_days"]) else None
        if not iso:
            return

        try:
            data = DataService.get_day_history(iso, patient_id=patient_id) or {}
            state["day_percent"] = int(data.get("adherence_percent", 0) or 0)
            state["day_items"] = data.get("items", []) or []
        except Exception as e:
            show_error(f"Erro ao carregar dia: {e}")

    def load_week():
        try:
            week = DataService.get_week_history(patient_id=patient_id) or {}
            # week: {start_date, days, dates, weekly_data, average}
            state["average"] = int(week.get("average", 0) or 0)

            state["days"] = week.get("days", []) or ["", "", "", "", "", "", ""]
            state["dates"] = week.get("dates", []) or ["", "", "", "", "", "", ""]
            state["weekly_data"] = week.get("weekly_data", []) or [0, 0, 0, 0, 0, 0, 0]

            start_iso = week.get("start_date")
            if start_iso:
                start_d = date.fromisoformat(start_iso)
            else:
                start_d = date.today() - timedelta(days=6)

            state["iso_days"] = [(start_d + timedelta(days=i)).isoformat() for i in range(7)]

            # Seleciona o último dia por padrão
            state["selected_index"] = 6
            load_day_by_index(state["selected_index"])

        except Exception as e:
            show_error(f"Erro ao carregar semana: {e}")

    # ---------------- Render / Interaction ----------------
    def change_day(idx: int):
        state["selected_index"] = idx
        load_day_by_index(idx)
        history_container.content = build_content()
        history_container.update()

    def build_content():
        avg = int(state["average"] or 0)

        # Lista do dia
        items_controls = []
        if not state["day_items"]:
            items_controls.append(
                ft.Text("Sem registros nesse dia.", color=AppColors.SECONDARY)
            )
        else:
            for it in state["day_items"]:
                items_controls.append(
                    med_item(
                        it.get("medicine_name", "Remédio"),
                        it.get("time", "--:--"),
                        it.get("status", "pending"),
                    )
                )

        return ft.Column(
            spacing=18,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text(
                    "Adesão dos últimos 7 dias",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.SECONDARY,
                ),
                ft.Text(
                    f"{avg}%",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=average_color(avg),
                ),
                build_chart(state["weekly_data"]),
                build_day_selector(),
                ft.Divider(),

                ft.Text(
                    f"Adesão do dia: {int(state['day_percent'] or 0)}%",
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.SECONDARY,
                ),
                *items_controls,
            ],
        )

    # Inicializa
    load_week()
    history_container.content = build_content()
    return history_container