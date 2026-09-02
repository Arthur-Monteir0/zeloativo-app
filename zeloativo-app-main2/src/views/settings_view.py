import flet as ft
from utils.theme import AppColors
from services.data_service import DataService

# ==========================================================
# COMPONENTES REUTILIZÁVEIS
# ==========================================================

def menu_item(icon, title, on_click, is_logout=False):
    color = ft.Colors.RED if is_logout else AppColors.SECONDARY

    return ft.ListTile(
        leading=ft.Icon(icon, color=color),
        title=ft.Text(title, color=color, weight=ft.FontWeight.BOLD),
        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color=color),
        on_click=on_click,  # ✅ funciona bem em versões antigas e novas
    )

def top_bar_with_back_right(title, on_back):
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text(title, size=24, weight="bold", color=AppColors.PRIMARY),
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=AppColors.PRIMARY,
                icon_size=20,
                on_click=lambda e: on_back(),
            ),
        ],
    )

# ==========================================================
# 1️⃣ TELA PRINCIPAL DE CONFIGURAÇÕES
# ==========================================================

def settings_main_view(page: ft.Page, on_profile, on_link, on_alert, on_logout):


    def logout_click(e):
        modal = None

        def close_modal(e=None):
            nonlocal modal
            if modal and modal in page.overlay:
                page.overlay.remove(modal)
                modal = None
                page.update()

        def confirm_logout(e=None):
            close_modal()
            on_logout()

        modal = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.55, ft.Colors.BLACK),
            alignment=ft.alignment.Alignment(0, 0),
            content=ft.Container(
                width=320,
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=16,
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.Text("Sair", size=18, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),
                        ft.Text(
                            "Você tem certeza que quer sair?",
                            color=AppColors.SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Text("Cancelar", color=AppColors.PRIMARY),
                                    bgcolor="#BFD8D6",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
                                    on_click=close_modal,
                                ),
                                ft.ElevatedButton(
                                    content=ft.Text("Sim, Sair", color=ft.Colors.WHITE),
                                    bgcolor="#FF3B30",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
                                    on_click=confirm_logout,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )

        page.overlay.append(modal)
        page.update()

    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=20,
        expand=True,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Meu Perfil",
                            size=26,
                            weight="bold",
                            color=AppColors.PRIMARY,
                        )
                    ],
                ),
                ft.Container(height=20),
                menu_item(ft.Icons.PERSON_OUTLINE, "Perfil", lambda e: on_profile()),
                ft.Divider(height=1, color="#E0E0E0"),
                menu_item(ft.Icons.FAVORITE_BORDER, "Vincular Dependentes", lambda e: on_link()),
                ft.Divider(height=1, color="#E0E0E0"),
                menu_item(ft.Icons.SETTINGS_OUTLINED, "Configurações", lambda e: on_alert()),
                ft.Divider(height=1, color="#E0E0E0"),
                menu_item(ft.Icons.LOGOUT, "Sair", logout_click, is_logout=True),
            ],
        ),
    )

# ==========================================================
# 2️⃣ PERFIL
# ==========================================================

def edit_profile_view(page: ft.Page, on_back):

    def input_field(label, placeholder):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Text(label, size=14, weight="bold", color=AppColors.SECONDARY),
                ft.TextField(
                    hint_text=placeholder,
                    bgcolor="#F5F7FB",
                    border_color=ft.Colors.TRANSPARENT,
                    border_radius=10,
                    filled=True,
                    color=AppColors.SECONDARY,
                ),
            ],
        )

    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=20,
        expand=True,
        content=ft.Column(
            spacing=20,
            controls=[
                top_bar_with_back_right("Perfil", on_back),
                input_field("Nome Completo", "Seu nome"),
                input_field("Número de Telefone", "+55 (00) 00000-0000"),
                input_field("Email", "seuemail@exemplo.com"),
                input_field("Data De Nascimento", "DD / MM / AAAA"),
                ft.Container(height=10),
                ft.ElevatedButton(
                    content=ft.Text(
                        "Atualizar Perfil",
                        color=ft.Colors.WHITE,
                        size=16,
                        weight="bold",
                    ),
                    bgcolor=AppColors.PRIMARY,
                    width=float("inf"),
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                ),
            ],
        ),
    )

# ==========================================================
# 3️⃣ VINCULAR DEPENDENTES
# ==========================================================

def link_dependent_view(page: ft.Page, on_back):

    codigo_input = ft.TextField(
        max_length=6,
        text_align=ft.TextAlign.CENTER,
        text_size=26,
        bgcolor="#F5F7FB",
        border_color=ft.Colors.TRANSPARENT,
        border_radius=10,
        filled=True,
        color=AppColors.SECONDARY,
        hint_text="EX: 4BXJS6",
        capitalization=ft.TextCapitalization.CHARACTERS,
    )

    def vincular(e):

        code = (codigo_input.value or "").strip().upper()

        if not code:
            page.snack_bar = ft.SnackBar(ft.Text("Digite o código"), open=True)
            page.update()
            return

        resp = DataService.accept_link_code(code)

        if resp.get("status_code") == 200:
            page.snack_bar = ft.SnackBar(ft.Text("Dependente vinculado com sucesso!"), open=True)
            codigo_input.value = ""
        else:
            detail = (resp.get("body") or {}).get("detail", "Erro ao vincular")
            page.snack_bar = ft.SnackBar(ft.Text(detail), open=True)

        page.update()

    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=20,
        expand=True,
        content=ft.Column(
            spacing=30,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                top_bar_with_back_right("Vincular", on_back),

                ft.Text(
                    "Digite o código de 6 caracteres gerado pelo aplicativo do dependente.",
                    size=16,
                    color=AppColors.SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),

                codigo_input,

                ft.ElevatedButton(
                    on_click=vincular,
                    content=ft.Text(
                        "Vincular Dependente",
                        color=ft.Colors.WHITE,
                        size=16,
                        weight="bold",
                    ),
                    bgcolor=AppColors.TERTIARY,
                    width=float("inf"),
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                ),
            ],
        ),
    )
# ==========================================================
# 4️⃣ CONFIGURAÇÕES DE ALERTA
# ==========================================================

def alert_settings_view(page: ft.Page, on_back):

    def toggle_item(label):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, size=16, weight="bold", color=AppColors.SECONDARY),
                ft.Switch(active_color=AppColors.PRIMARY, value=True),
            ],
        )

    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=20,
        expand=True,
        content=ft.Column(
            spacing=30,
            controls=[
                top_bar_with_back_right("Configurações", on_back),
                ft.Column(
                    spacing=25,
                    controls=[
                        toggle_item("Notificar antes do horário"),
                        toggle_item("Alerta sonoro alto"),
                        toggle_item("Vibrar dispositivo"),
                        toggle_item("Notificar cuidador se atrasar"),
                    ],
                ),
            ],
        ),
    )

# ==========================================================
# ✅ WRAPPER FINAL: ESTA É A FUNÇÃO QUE A HOME_VIEW VAI CHAMAR
# ==========================================================

def settings_view(page: ft.Page, on_logout):
    """
    Controla a navegação interna da aba Ajustes:
    main -> profile/link/alert -> back -> main
    """

    state = {"screen": "main"}  # main | profile | link | alert
    root = ft.Container(expand=True, bgcolor=ft.Colors.WHITE)

    def go(screen: str):
        state["screen"] = screen
        render()

    def render():
        if state["screen"] == "main":
            root.content = settings_main_view(
                page=page,
                on_profile=lambda: go("profile"),
                on_link=lambda: go("link"),
                on_alert=lambda: go("alert"),
                on_logout=on_logout,
            )
        elif state["screen"] == "profile":
            root.content = edit_profile_view(page, on_back=lambda: go("main"))
        elif state["screen"] == "link":
            root.content = link_dependent_view(page, on_back=lambda: go("main"))
        elif state["screen"] == "alert":
            root.content = alert_settings_view(page, on_back=lambda: go("main"))

        page.update()

    render()
    return root