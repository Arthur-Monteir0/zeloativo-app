import flet as ft
from utils.theme import AppColors

def screen(body: ft.Control, *, padding: int = 20, scroll=True):
    return ft.Container(
        expand=True,
        bgcolor=AppColors.BACKGROUND,
        padding=padding,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO if scroll else None,
            controls=[body],
        ),
    )