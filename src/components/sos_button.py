import flet as ft
from utils.theme import AppColors


def sos_button(page: ft.Page):
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(
                    ft.Icons.PHONE,
                    color=AppColors.BACKGROUND,
                    size=20,
                ),
                ft.Text(
                    "SOS",
                    color=AppColors.BACKGROUND,
                    weight="bold",
                    size=14,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        bgcolor=AppColors.ALERT,
        padding=ft.Padding.symmetric(horizontal=15, vertical=10),
        border_radius=30,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color="rgba(0,0,0,0.3)",
        ),
        on_click=lambda _: page.launch_url("tel:190"),
        right=20,
        top=20,
    )