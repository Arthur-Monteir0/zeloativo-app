import flet as ft
from utils.theme import AppColors

def auth_login_view(page: ft.Page, go_to_register, go_to_home):
    email = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    password = ft.TextField(label="Senha", password=True, can_reveal_password=True)

    return ft.Container(
        expand=True,
        bgcolor=AppColors.BACKGROUND,
        padding=ft.padding.all(24),
        content=ft.Column(
            spacing=18,
            controls=[
                ft.Text("Entrar", size=26, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),

                ft.Row(
                    spacing=5,
                    controls=[
                        ft.Text("Não tem uma conta?", color=AppColors.SECONDARY),
                        ft.TextButton(
                            "Criar conta!",
                            style=ft.ButtonStyle(color=AppColors.PRIMARY),
                            on_click=lambda e: go_to_register(),
                        ),
                    ],
                ),

                email,
                password,

                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.TextButton(
                            "Esqueceu a senha?",
                            style=ft.ButtonStyle(color=AppColors.SECONDARY),
                            on_click=lambda e: print("Reset senha (futuro)"),
                        )
                    ],
                ),

                ft.Container(height=20),

                ft.ElevatedButton(
                    "Entrar",
                    width=float("inf"),
                    height=50,
                    bgcolor=AppColors.PRIMARY,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: go_to_home(),
                ),
            ],
        ),
    )