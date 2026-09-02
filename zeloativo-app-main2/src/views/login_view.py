import flet as ft
from utils.theme import AppColors

def login_view(page: ft.Page, go_to_register, go_to_auth_login):
    return ft.Stack(
        expand=True,
        controls=[
            # Fundo principal
            ft.Container(expand=True, bgcolor=AppColors.PRIMARY),

            # Onda superior esquerda
            ft.Container(
                width=280,
                height=280,
                bgcolor=AppColors.SECONDARY,
                border_radius=ft.BorderRadius.only(bottom_right=200),
                left=-60,
                top=-60,
            ),

            # Onda inferior direita
            ft.Container(
                width=320,
                height=320,
                bgcolor=AppColors.SECONDARY,
                border_radius=ft.BorderRadius.only(top_left=220),
                right=-80,
                bottom=-80,
            ),

            # Conteúdo central
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=18,
                    controls=[
                        ft.Image(src="assets/logo.png", width=120, height=120),

                        ft.Text(
                            "ZeloAtivo",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.TEXT_ON_PRIMARY,
                        ),

                        ft.Text(
                            "Nunca mais esqueça sua medicação",
                            size=16,
                            color=AppColors.TEXT_ON_PRIMARY,
                            text_align=ft.TextAlign.CENTER,
                        ),

                        ft.Container(height=30),

                        # ✅ Entrar -> vai para login real
                        ft.ElevatedButton(
                            "Entrar",
                            width=250,
                            height=55,
                            bgcolor=AppColors.TERTIARY,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: go_to_auth_login(),
                        ),

                        # ✅ Criar conta -> cadastro
                        ft.ElevatedButton(
                            "Criar conta",
                            width=250,
                            height=55,
                            bgcolor=AppColors.SECONDARY,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: go_to_register(),
                        ),
                    ],
                ),
            ),
        ],
    )