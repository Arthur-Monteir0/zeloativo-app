import flet as ft
from utils.theme import AppColors
from services.auth_service import AuthService
from services.data_service import DataService


def auth_login_view(page: ft.Page, go_to_register, go_to_home, storage_set):
    email = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    password = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    msg = ft.Text("", color=ft.Colors.RED)

    def show_snack(text: str):
        page.snack_bar = ft.SnackBar(ft.Text(text), open=True)
        page.update()

    def entrar(e):
        try:
            res = AuthService.login(email.value.strip(), password.value)
            token = res.get("access_token")

            if not token:
                msg.value = "Login OK, mas não veio access_token."
                page.update()
                return

            DataService.set_token(token)
            storage_set("access_token", token)

            go_to_home()
            page.update()

        except Exception as err:
            msg.value = str(err)
            page.update()

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
                msg,

                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.TextButton(
                            "Esqueceu a senha?",
                            style=ft.ButtonStyle(color=AppColors.SECONDARY),
                            on_click=lambda e: show_snack("Reset de senha: implementar depois"),
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
                    on_click=entrar,
                ),
            ],
        ),
    )