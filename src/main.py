import flet as ft

from utils.theme import get_app_theme
from components.navigation import navigation_bar
from components.sos_button import sos_button
from views.history_view import history_view
from views.login_view import login_view
from views.register_view import register_view
from views.auth_login_view import auth_login_view


def main(page: ft.Page):
    page.title = "ZeloAtivo"
    page.theme = get_app_theme()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 844
    page.padding = 0
    page.spacing = 0

    # ---------------- LAYOUT PRINCIPAL DO APP ----------------
    def load_app_layout(content_view, nav_index=0):
        page.controls.clear()
        page.overlay.clear()

        page.overlay.append(sos_button(page))

        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=content_view,
                        expand=True,
                        padding=ft.Padding.only(
                            top=80,
                            left=20,
                            right=20,
                            bottom=10,
                        ),
                    ),
                    navigation_bar(nav_index, on_nav_change),
                ],
                expand=True,
                spacing=0,
            )
        )

        page.update()

    # ---------------- NAVEGAÇÃO ----------------
    def on_nav_change(index):
        if index == 0:
            go_to_home()

        elif index == 1:
            load_app_layout(
                ft.Text(
                    "Tela em desenvolvimento",
                    size=20,
                ),
                nav_index=index,
            )

        elif index == 2:
            # ✅ CORREÇÃO AQUI
            load_app_layout(history_view(page), nav_index=2)

        else:
            load_app_layout(
                ft.Text("Tela futura"),
                nav_index=index,
            )

    # ---------------- TELAS DE LOGIN ----------------
    def go_to_login_initial():
        page.controls.clear()
        page.overlay.clear()
        page.add(login_view(page, go_to_register, go_to_auth_login))
        page.update()

    def go_to_register():
        page.controls.clear()
        page.overlay.clear()
        page.add(register_view(page, go_to_auth_login, go_to_home))
        page.update()

    def go_to_auth_login():
        page.controls.clear()
        page.overlay.clear()
        page.add(auth_login_view(page, go_to_register, go_to_home))
        page.update()

    # ---------------- HOME ----------------
    def go_to_home():
        home_content = ft.Column(
            [
                ft.Text(
                    "Início do ZeloAtivo",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Sua lista de doses aparecerá aqui.",
                    size=16,
                ),
            ],
            spacing=10,
        )

        load_app_layout(home_content, nav_index=0)

    # Tela inicial
    go_to_login_initial()


ft.run(main)