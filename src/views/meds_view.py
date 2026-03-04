import flet as ft
from utils.theme import AppColors

def meds_view(page: ft.Page):
    page.bgcolor = "#FFFFFF"

    # ==========================================================
    # FORMULÁRIO (ADD / EDIT)
    # ==========================================================
    def open_form(modo="add", nome_medicamento=""):

        nome = ft.TextField(label="Nome", value=nome_medicamento if modo == "edit" else "")
        dosagem = ft.TextField(label="Dosagem", value="500mg" if modo == "edit" else "")
        observacao = ft.TextField(
            label="Observação",
            value="Tomar após refeição" if modo == "edit" else "",
            multiline=True,
        )

        intervalo = ft.Dropdown(
            label="Intervalo",
            value="8" if modo == "edit" else None,
            options=[
                ft.dropdown.Option("6"),
                ft.dropdown.Option("8"),
                ft.dropdown.Option("12"),
                ft.dropdown.Option("24"),
            ],
        )

        data_inicio = ft.TextField(label="Data início", value="2026-03-03" if modo == "edit" else "")
        hora_inicio = ft.TextField(label="Hora início", value="08:00" if modo == "edit" else "")
        data_fim = ft.TextField(label="Data fim", value="2026-03-10" if modo == "edit" else "")

        
        def fechar(e=None):
            sheet.open = False
            page.update()

        # BOTÕES INFERIORES
        botoes = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.ElevatedButton(
                    "Salvar",
                    expand=True,
                    height=55,
                    bgcolor=AppColors.PRIMARY,
                    color=AppColors.SECONDARY,
                    on_click=fechar, 
                ),
                ft.Container(width=10),
                ft.ElevatedButton(
                    "Excluir",
                    expand=True,
                    height=55,
                    bgcolor="red",
                    color="white",
                    visible=True if modo == "edit" else False,
                    on_click=fechar, 
                ),
            ],
        )

        # CARD IMAGEM DIFERENTE PARA ADD
        if modo == "add":
            imagem_card = ft.Container(
                height=140,
                bgcolor="#F2F2F2",
                border_radius=15,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.CAMERA_ALT, size=40, color="gray"),
                        ft.Text("Toque para adicionar imagem", color="gray"),
                    ],
                ),
                on_click=lambda e: print("Abriria câmera/galeria"),
            )
        else:
            imagem_card = ft.Container(
                height=140,
                bgcolor="#F2F2F2",
                border_radius=15,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Text("Imagem do medicamento")],
                ),
            )

        sheet = ft.BottomSheet(
            content=ft.Container(
                height=page.window_height * 0.95,
                bgcolor="#FFFFFF",
                padding=20,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        # TOPO
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=fechar, 
                                ),
                                ft.Text(
                                    "Editar Medicação" if modo == "edit" else "Adicionar Medicação",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppColors.SECONDARY,
                                ),
                            ],
                        ),

                        ft.Container(height=20),
                        imagem_card,
                        ft.Container(height=20),

                        nome,
                        dosagem,
                        observacao,
                        intervalo,
                        data_inicio,
                        hora_inicio,
                        data_fim,

                        ft.Container(height=25),
                        botoes,
                    ],
                ),
            )
        )

        page.overlay.append(sheet)
        sheet.open = True
        page.update()

    # ==========================================================
    # CARD MEDICAMENTO
    # ==========================================================
    def med_card(nome):
        return ft.Container(
            padding=20,
            border=ft.border.all(1.5, AppColors.PRIMARY),
            border_radius=20,
            margin=ft.margin.only(bottom=18),
            bgcolor="#FFFFFF",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        nome,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.SECONDARY,
                    ),
                    ft.OutlinedButton(
                        "Editar",
                        icon=ft.Icons.EDIT,
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1.5, AppColors.PRIMARY),
                            shape=ft.RoundedRectangleBorder(radius=25),
                        ),
                        on_click=lambda e: open_form("edit", nome),
                    ),
                ],
            ),
        )

    # ==========================================================
    # LAYOUT PRINCIPAL
    # ==========================================================
    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                # IMAGEM TOPO
                ft.Container(
                    height=190,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    border_radius=ft.border_radius.only(
                        bottom_left=35,
                        bottom_right=35,
                    ),
                    content=ft.Image(
                        src=page.assets_dir + "/remedio.jpeg",
                        fit="cover",
                        width=float("inf"),
                        height=190,
                    ),
                ),

                ft.Container(
                    padding=20,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Meus Remédios",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.SECONDARY,
                            ),

                            ft.Text(
                                "Gerencie sua medicação",
                                size=16,
                                color=AppColors.SECONDARY,
                            ),

                            ft.Container(height=20),

                            med_card("Losartana 50mg"),
                            med_card("Dipirona 1g"),

                            ft.Container(height=30),

                        
                            ft.ElevatedButton(
                                "Adicionar medicação",
                                width=float("inf"), 
                                height=70,
                                bgcolor=AppColors.PRIMARY,
                                color=AppColors.SECONDARY,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=35),
                                ),
                                on_click=lambda e: open_form("add"),
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )