import flet as ft
from utils.theme import AppColors


def history_view(page: ft.Page):

    weekly_data = [100, 75, 100, 50, 100, 100, 80]
    days = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]
    dates = ["1", "2", "3", "4", "5", "6", "7"]

    selected_index = 3

    # 🔹 FUNDO
    history_container = ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        padding=20,
    )

    def change_day(index):
        nonlocal selected_index
        selected_index = index
        history_container.content = build_content()
        history_container.update()

    def med_item(name, time, status):

        if status == "taken":
            icon = ft.Icons.CHECK_CIRCLE
            color = "green"
            status_text = "+100%"
        elif status == "pending":
            icon = ft.Icons.ACCESS_TIME
            color = "orange"
            status_text = "Pendente"
        else:
            icon = ft.Icons.CANCEL
            color = "red"
            status_text = "Perdida"

        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=color, size=28),
                    ft.Column(
                        [
                            ft.Text(name, weight=ft.FontWeight.BOLD),
                            ft.Text(time, size=12),
                        ],
                        expand=True,
                    ),
                    ft.Text(status_text, color=color, weight=ft.FontWeight.BOLD),
                ]
            ),
            padding=15,
            border_radius=12,
            bgcolor="#F5F7FA",
        )

    def build_content():

        average = sum(weekly_data) / len(weekly_data)
        average_text = f"{average:.0f}%"
        average_color = "green" if average >= 60 else "red"

        # ---------- SELETOR ----------
        day_buttons = []

        for i in range(7):
            is_selected = i == selected_index

            day_buttons.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                dates[i],
                                weight=ft.FontWeight.BOLD,
                                color="white" if is_selected else AppColors.SECONDARY,
                            ),
                            ft.Text(
                                days[i],
                                size=10,
                                color="white" if is_selected else AppColors.SECONDARY,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10,
                    border_radius=20,
                    # 🔹 CINZA CLARO QUANDO NÃO SELECIONADO
                    bgcolor=AppColors.SECONDARY if is_selected else "#F2F2F2",
                    on_click=lambda e, idx=i: change_day(idx),
                )
            )

        day_selector = ft.Row(
            day_buttons,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        # ---------- GRÁFICO ----------
        bars = [
            ft.Container(
                width=22,
                height=value * 1.3,
                bgcolor=AppColors.PRIMARY,
                border_radius=6,
            )
            for value in weekly_data
        ]

        chart = ft.Container(
            content=ft.Row(
                bars,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
            height=180,
        )

        return ft.Column(
            [
                ft.Text(
                    "Adesão dos últimos 7 dias",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    average_text,
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=average_color,
                ),
                chart,
                day_selector,
                ft.Divider(),
                ft.Text(
                    f"Adesão do dia: {weekly_data[selected_index]}%",
                    weight=ft.FontWeight.BOLD,
                ),
                med_item("Metformina", "08:00", "taken"),
                med_item("Sinvastatina", "12:00", "taken"),
                med_item("Enalapril", "18:00", "taken"),
                med_item("Losartana", "20:00", "pending"),
                med_item("AAS", "22:00", "missed"),
            ],
            spacing=18,
            scroll=ft.ScrollMode.AUTO,
        )

    history_container.content = build_content()

    return history_container