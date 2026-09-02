import flet as ft
from utils.theme import AppColors
from services.auth_service import AuthService
from services.data_service import DataService


def register_view(page, go_to_login, go_to_home, storage_set):
    name = ft.TextField(label="Nome completo")
    email = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    phone = ft.TextField(label="Contato", keyboard_type=ft.KeyboardType.PHONE)
    password = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    confirm_password = ft.TextField(label="Confirmar senha", password=True, can_reveal_password=True)

    msg = ft.Text("", color=ft.Colors.RED)

    def show_snack(text: str):
        page.snack_bar = ft.SnackBar(ft.Text(text), open=True)
        page.update()

    def cadastrar(e):
        if not name.value.strip():
            msg.value = "Digite seu nome."
            page.update()
            return
        if not email.value.strip():
            msg.value = "Digite seu email."
            page.update()
            return
        if not password.value:
            msg.value = "Digite uma senha."
            page.update()
            return
        if password.value != confirm_password.value:
            msg.value = "As senhas não conferem."
            page.update()
            return

        msg.value = ""
        page.update()

        try:
            res = AuthService.register(
                email=email.value.strip(),
                password=password.value,
                full_name=name.value.strip(),
                phone=phone.value.strip() if phone.value else None,
                role="patient",
            )

            token = res.get("access_token")

            # Se o Supabase estiver configurado sem confirmação de email, ele já devolve token
            if token:
                DataService.set_token(token)
                storage_set("access_token", token)
                go_to_home()
                return

            # Caso típico: precisa confirmar email
            show_snack("Conta criada! Confirme no email e depois faça login.")
            go_to_login()

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
                ft.Text("Criar conta", size=26, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),
                ft.Row(
                    spacing=5,
                    controls=[
                        ft.Text("Já tem uma conta?", color=AppColors.SECONDARY),
                        ft.TextButton(
                            "Entrar!",
                            style=ft.ButtonStyle(color=AppColors.PRIMARY),
                            on_click=lambda e: go_to_login(),
                        ),
                    ],
                ),
                name,
                email,
                phone,
                password,
                confirm_password,
                msg,
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Cadastrar",
                    width=float("inf"),
                    height=50,
                    bgcolor=AppColors.PRIMARY,
                    color=ft.Colors.WHITE,
                    on_click=cadastrar,
                ),
            ],
        ),
    )