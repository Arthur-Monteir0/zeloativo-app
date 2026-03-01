# main.py
# Entry point and route management
import flet as ft
from utils.theme import get_app_theme, AppColors

def main(page: ft.Page):
    page.title = "ZeloAtivo"
    page.theme = get_app_theme()
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Configuração de responsividade para Mobile
    page.window_width = 390
    page.window_height = 844

    def on_navigation_change(e):
        index = e.control.selected_index
        if index == 0: page.go("/")
        elif index == 1: page.go("/meds")
        elif index == 2: page.go("/history")
        elif index == 3: page.go("/shared")
        elif index == 4: page.go("/settings")

    def route_change(route):
        page.views.clear()
        
        # BARRA DE NAVEGAÇÃO (Reutilizável)
        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME, label="Início"),
                ft.NavigationDestination(icon=ft.icons.MEDICATION_OUTLINED, label="Remédios"),
                ft.NavigationDestination(icon=ft.icons.INSERT_CHART_OUTLINED, label="Histórico"),
                ft.NavigationDestination(icon=ft.icons.PEOPLE_OUTLINED, label="Compartilhados"),
                ft.NavigationDestination(icon=ft.icons.SETTINGS_OUTLINED, label="Ajustes"),
            ],
            on_change=on_navigation_change,
        )

        # BOTÃO SOS (Sempre visível na Home)
        sos_button = ft.FloatingActionButton(
            content=ft.Text("SOS", color="white", weight="bold"),
            bgcolor=AppColors.ALERT,
            on_click=lambda _: print("Abrir Teclado: ligar para cuidador"),
        )

        # ROTEAMENTO
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("ZeloAtivo"), bgcolor=AppColors.PRIMARY),
                        ft.Text("Próximas Doses", style="displayLarge"),
                        # Aqui entrará a lista de cards
                        ft.Column(expand=True, scroll=ft.ScrollMode.AUTO), 
                    ],
                    navigation_bar=nav_bar,
                    floating_action_button=sos_button,
                )
            )
        elif page.route == "/meds":
            page.views.append(
                ft.View("/meds", [ft.AppBar(title=ft.Text("Meus Remédios")), ft.Text("Tela de Cadastro")], navigation_bar=nav_bar)
            )
        # Adicionar outras rotas conforme o desenvolvimento...
        
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)