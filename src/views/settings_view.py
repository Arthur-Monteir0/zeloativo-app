import flet as ft
from utils.theme import AppColors

# ==========================================================
# COMPONENTES REUTILIZÁVEIS
# ==========================================================

def menu_item(icon, text, on_click, is_logout=False):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=AppColors.ALERT if is_logout else AppColors.PRIMARY),
                ft.Text(
                    text,
                    size=16,
                    weight="bold",
                    color=AppColors.ALERT if is_logout else AppColors.SECONDARY,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.CHEVRON_RIGHT,
                    color=AppColors.ALERT if is_logout else AppColors.SECONDARY,
                ),
            ]
        ),
        padding=ft.padding.symmetric(vertical=20, horizontal=15),
        on_click=on_click,
        ink=True,
        border_radius=10,
        bgcolor=ft.Colors.TRANSPARENT,
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

    def fechar_dialog(dialog):
        dialog.open = False
        page.update()

    def confirmar_logout(dialog):
        dialog.open = False
        page.update()

        # Limpa overlay inteiro (remove dialog + SOS temporariamente)
        page.overlay.clear()

        # Executa logout absoluto
        on_logout()

    def logout_click(e):

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Sair",
                weight="bold",
                color=AppColors.SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Text(
                "Você tem certeza que quer sair?",
                color=AppColors.SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
            actions=[
                ft.ElevatedButton(
                    content=ft.Text("Cancelar", color=AppColors.PRIMARY),
                    bgcolor="#BFD8D6",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25)
                    ),
                    on_click=lambda e: fechar_dialog(dialog),
                ),
                ft.ElevatedButton(
                    content=ft.Text("Sim, Sair", color=ft.Colors.WHITE),
                    bgcolor="#FF3B30",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25)
                    ),
                    on_click=lambda e: confirmar_logout(dialog),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=15),
            bgcolor=ft.Colors.WHITE,
        )

       
        page.overlay.append(dialog)
        dialog.open = True
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
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                ),
            ],
        ),
    )

# ==========================================================
# 3️⃣ VINCULAR DEPENDENTES
# ==========================================================

def link_dependent_view(page: ft.Page, on_back):

    codigo_input = ft.TextField(
        max_length=4,
        text_align=ft.TextAlign.CENTER,
        text_size=30,
        bgcolor="#F5F7FB",
        border_color=ft.Colors.TRANSPARENT,
        border_radius=10,
        filled=True,
        color=AppColors.SECONDARY,
        hint_text="0000",
    )

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
                    "Digite o código de 4 dígitos gerado pelo aplicativo do seu dependente.",
                    size=16,
                    color=AppColors.SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                codigo_input,
                ft.ElevatedButton(
                    content=ft.Text(
                        "Vincular Dependentes",
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