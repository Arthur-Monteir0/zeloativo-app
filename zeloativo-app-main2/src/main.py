import flet as ft
import json
import os

from views.settings_view import settings_view
from utils.theme import get_app_theme
from components.navigation import navigation_bar
from components.sos_button import sos_button

from services.data_service import DataService
from views.home_view import home_view
from views.login_view import login_view
from views.history_view import history_view
from views.register_view import register_view
from views.auth_login_view import auth_login_view
from views.shared_view import SharedView
from views.meds_view import meds_view
from views.vinculo_view import vinculo_view
from views.historico_dependentes_view import historico_dependentes_view

from services.alarm_service import AlarmService, AlarmConfig

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

    # ✅ Instância do alarme (uma vez)
    alarm = AlarmService(page, AlarmConfig(minutes_before=5, check_interval_sec=20))

    # ---------------- STORAGE COMPATÍVEL ----------------
    TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")

    def storage_get(key: str):
        if hasattr(page, "client_storage") and page.client_storage:
            return page.client_storage.get(key)
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get(key)
            except: return None
        return None

    def storage_set(key: str, value):
        if hasattr(page, "client_storage") and page.client_storage:
            page.client_storage.set(key, value)
            return
        data = {}
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except: pass
        data[key] = value
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def storage_remove(key: str):
        if hasattr(page, "client_storage") and page.client_storage:
            page.client_storage.remove(key)
            return
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data.pop(key, None)
                with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f)
            except: pass

    # ---------------- HELPERS ----------------
    def is_logged_in() -> bool:
        return bool(DataService.token)

    def show_snack(text: str):
        page.snack_bar = ft.SnackBar(ft.Text(text), open=True)
        page.update()

    def logout():
        close_dialog()
        alarm.stop()  # ✅ DESLIGA O ALARME
        DataService.set_token(None)
        storage_remove("access_token")
        show_snack("Você saiu da conta.")
        go_to_login_initial()

    def require_login():
        if not is_logged_in():
            go_to_login_initial()
            return False
        return True

    # ---------------- FUNÇÃO LAYOUT PRINCIPAL ----------------
    def load_app_layout(content_view, nav_index=0):
        page.controls.clear()
        page.overlay.clear() # Limpa overlays anteriores (importante para o SOS)

        # Botão SOS sempre visível nas telas logadas
        page.overlay.append(sos_button(page))

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[ft.Text("ZeloAtivo", size=18, weight=ft.FontWeight.BOLD)],
        )

        page.add(
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    ft.Container(
                        expand=True,
                        padding=ft.Padding.only(top=50, left=20, right=20, bottom=10),
                        content=ft.Column(
                            expand=True,
                            spacing=10,
                            controls=[
                                top_bar,
                                ft.Container(expand=True, content=content_view),
                            ],
                        ),
                    ),
                    navigation_bar(nav_index, on_nav_change),
                ],
            )
        )
        page.update()

    # ---------------- NAVEGAÇÃO ----------------
    def on_nav_change(index):
        if not require_login():
            return

        if index == 0:
            go_to_home()
        elif index == 1:
            load_app_layout(meds_view(page), nav_index=1)
        elif index == 2:
            load_app_layout(history_view(page), nav_index=2)
        elif index == 3:
            links = DataService.my_links() or {}
            print("DEBUG links:", links)

            patients = links.get("patients", []) or []
            print("DEBUG patients:", patients)
            def ir_para_vinculo():
                load_app_layout(
                    vinculo_view(page, on_back_click=lambda: on_nav_change(3)),
                    nav_index=3
                )

            try:
                links = DataService.my_links() or {}
                patients = links.get("patients", []) or []
            except Exception:
                patients = []

            if patients:
                patient_id = patients[0]["patient_user_id"]
                print("DEBUG abrindo historico_dependentes_view, patient_id:", patient_id)
                load_app_layout(historico_dependentes_view(page,patient_id,on_unlinked=lambda: on_nav_change(3)),nav_index=3)
            else:
                load_app_layout(SharedView(page, ir_para_vinculo), nav_index=3)
        elif index == 4:
            load_app_layout(settings_view(page, logout), nav_index=4)

    # ---------------- TELAS ----------------
    def close_dialog():
        if getattr(page, "dialog", None):
            page.dialog.open = False
            page.dialog = None
    def go_to_home():
        if not require_login():
            return
        alarm.start()
        load_app_layout(home_view(page), nav_index=0)


    def go_to_auth_login():
        close_dialog()
        page.controls.clear()
        page.overlay.clear()
        page.add(auth_login_view(page, go_to_register, go_to_home, storage_set))
        page.update()

    def go_to_register():
        close_dialog()
        page.controls.clear()
        page.overlay.clear()
        page.add(register_view(page, go_to_auth_login, go_to_home, storage_set))
        page.update()

    def go_to_login_initial():
        close_dialog()
        page.controls.clear()
        page.overlay.clear()
        page.add(login_view(page, go_to_register, go_to_auth_login))
        page.update()

    # ---------------- AUTO-LOGIN ----------------
    saved_token = storage_get("access_token")
    if saved_token:
        DataService.set_token(saved_token)
        alarm.start()
        go_to_home()
    else:
        go_to_login_initial()

if __name__ == "__main__":
    ft.app(target=main) # ft.run é legado em versões novas, use ft.app