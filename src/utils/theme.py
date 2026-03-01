# theme.py
import flet as ft

class AppColors:
    PRIMARY = "#5CC6BA"
    SECONDARY = "#092C4C"
    BACKGROUND = "#FFFFFF"
    ALERT = "#FF222D"
    TEXT_ON_PRIMARY = "#092C4C" # Texto escuro sobre o verde para ler melhor

def get_app_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=AppColors.PRIMARY,
            secondary=AppColors.SECONDARY,
            error=AppColors.ALERT,
            background=AppColors.BACKGROUND,
        ),
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(size=32, weight="bold", color=AppColors.SECONDARY),
            body_large=ft.TextStyle(size=18, color=AppColors.SECONDARY),
        )
    )
