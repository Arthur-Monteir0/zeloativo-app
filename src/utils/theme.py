#theme.py
import flet as ft

class AppColors:
    PRIMARY = "#5CC6BA"       # Verde água (Zelo)
    SECONDARY = "#092C4C"     # Azul escuro (Confiança)
    TERTIARY = "#FF7F50"      # Coral (CTA principal)
    BACKGROUND = "#FFFFFF"
    ALERT = "#FF222D"         # Vermelho SOS
    TEXT_ON_PRIMARY = "#092C4C"


def get_app_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=AppColors.PRIMARY,
            secondary=AppColors.SECONDARY,
            error=AppColors.ALERT,
            surface=AppColors.BACKGROUND, 
        ),
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(size=32, weight="bold", color=AppColors.SECONDARY),
            body_large=ft.TextStyle(size=18, color=AppColors.SECONDARY),
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
    )