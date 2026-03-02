import flet as ft
from utils.theme import get_app_theme
from views.login_view import login_view              # Tela inicial (logo + botões)
from views.register_view import register_view        # Criar conta
from views.auth_login_view import auth_login_view    # Entrar (email/senha)

def main(page: ft.Page):
    page.title = "ZeloAtivo"
    page.theme = get_app_theme()
    page.padding = 0
    page.window_width = 390
    page.window_height = 844
    page.theme_mode = ft.ThemeMode.LIGHT

    def go_to_initial():
        page.controls.clear()
        page.add(login_view(page, go_to_register, go_to_auth_login))
        page.update()

    def go_to_register():
        page.controls.clear()
        page.add(register_view(page, go_to_auth_login, go_to_home))
        page.update()

    def go_to_auth_login():
        page.controls.clear()
        page.add(auth_login_view(page, go_to_register, go_to_home))
        page.update()

    def go_to_home():
        page.controls.clear()
        page.add(ft.Text("Home (em construção)", size=24))
        page.update()

    go_to_initial()

ft.run(main)