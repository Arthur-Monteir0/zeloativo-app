import flet as ft
from utils.theme import get_app_theme
from components.navigation import navigation_bar
from components.sos_button import sos_button

from views.history_view import history_view
from views.login_view import login_view
from views.register_view import register_view
from views.auth_login_view import auth_login_view
from views.shared_view import SharedView
from views.meds_view import meds_view
from views.vinculo_view import vinculo_view 

# ✅ Importando as novas views de configurações
from views.settings_view import settings_main_view, edit_profile_view, link_dependent_view, alert_settings_view

def main(page: ft.Page):
    # ---------------- CONFIGURAÇÕES GERAIS ----------------

    page.title = "ZeloAtivo"
    page.theme = get_app_theme()
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window_width = 390
    page.window_height = 844

    page.padding = 0
    page.spacing = 0

    page.assets_dir = "assets"
    page.bgcolor = ft.Colors.WHITE

    # ---------------- FUNÇÃO LAYOUT PRINCIPAL ----------------

    def load_app_layout(content_view, nav_index=0):
        page.controls.clear()
        page.overlay.clear()

        # Botão SOS sempre visível
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

    # ---------------- TELAS PRINCIPAIS ----------------

    def go_to_home():
        home_content = ft.Column(
            [
                ft.Text("Início do ZeloAtivo", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Sua lista de doses aparecerá aqui.", size=18),
            ],
            spacing=10,
        )
        load_app_layout(home_content, nav_index=0)

    def on_nav_change(index):
        if index == 0:
            go_to_home()

        elif index == 1:
            load_app_layout(meds_view(page), nav_index=1)

        elif index == 2:
            load_app_layout(history_view(page), nav_index=2)

        elif index == 3:
            # LÓGICA DE NAVEGAÇÃO DUPLA (INFO <-> CÓDIGO)
            def ir_para_gerar_codigo():
                load_app_layout(vinculo_view(page, on_back_click=ir_para_info), nav_index=3)

            def ir_para_info():
                load_app_layout(SharedView(page, on_vincular_click=ir_para_gerar_codigo), nav_index=3)

            ir_para_info()

        elif index == 4:
            # ✅ LÓGICA DE NAVEGAÇÃO DA ABA CONFIGURAÇÕES
            
            def ir_para_perfil():
                load_app_layout(edit_profile_view(page, on_back=ir_para_main_settings), nav_index=4)

            def ir_para_vincular_dep():
                load_app_layout(link_dependent_view(page, on_back=ir_para_main_settings), nav_index=4)

            def ir_para_alertas():
                load_app_layout(alert_settings_view(page, on_back=ir_para_main_settings), nav_index=4)

            def ir_para_main_settings():
                # A função settings_main_view recebe os comandos para onde cada botão deve ir
                load_app_layout(
                    settings_main_view(
                        page, 
                        on_profile=ir_para_perfil, 
                        on_link=ir_para_vincular_dep, 
                        on_alert=ir_para_alertas, 
                        on_logout=go_to_login_initial # Volta pro início absoluto!
                    ), 
                    nav_index=4
                )

            # Inicia mostrando o menu principal de configurações
            ir_para_main_settings()

    # ---------------- FLUXO DE AUTENTICAÇÃO ----------------

    def go_to_auth_login():
        page.controls.clear()
        page.overlay.clear()
        page.add(auth_login_view(page, go_to_register, go_to_home))
        page.update()

    def go_to_register():
        page.controls.clear()
        page.overlay.clear()
        page.add(register_view(page, go_to_auth_login, go_to_home))
        page.update()

    def go_to_login_initial():
        page.controls.clear()
        page.overlay.clear()
        page.add(login_view(page, go_to_register, go_to_auth_login))
        page.update()

    # Inicia pelo login
    go_to_login_initial()


if __name__ == "__main__":
    ft.run(main)