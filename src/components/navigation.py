import flet as ft
from utils.theme import AppColors


def navigation_bar(current_index: int, on_nav_change):
    nav_items = [
        {"icon": ft.Icons.HOME, "label": "Início"},
        {"icon": ft.Icons.MEDICATION, "label": "Remédios"},
        {"icon": ft.Icons.BAR_CHART, "label": "Histórico"},
        {"icon": ft.Icons.PEOPLE, "label": "Compartilhados"},
        {"icon": ft.Icons.SETTINGS, "label": "Ajustes"},
    ]

    def build_item(index, item):
        is_active = index == current_index
        color = AppColors.PRIMARY if is_active else AppColors.SECONDARY

        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(item["icon"], color=color, size=24),
                    ft.Text(
                        item["label"],
                        size=10,
                        color=color,
                        weight="bold" if is_active else "normal",
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            on_click=lambda _: on_nav_change(index),
            expand=True,
            padding=ft.Padding.symmetric(vertical=10),
        )

    return ft.Container(
        content=ft.Row(
            [build_item(i, item) for i, item in enumerate(nav_items)],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=AppColors.BACKGROUND,
        border=ft.border.only(
            top=ft.BorderSide(1, AppColors.PRIMARY)
        ),
        height=70,
    )