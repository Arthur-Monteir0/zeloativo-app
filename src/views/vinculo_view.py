import flet as ft
import random
from utils.theme import AppColors

def vinculo_view(page: ft.Page):
    # Gerador de código temporário
    codigo_vinculo = str(random.randint(1000, 9999))

    def copiar_codigo(e):
        page.set_clipboard(codigo_vinculo)
        page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Código copiado para a área de transferência!"))
        )

    # Aqui criamos as 4 caixinhas separadas dinamicamente
    caixinhas_codigo = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15, 
        controls=[
            ft.Container(
                content=ft.Text(digito, size=40, weight="bold", color=AppColors.SECONDARY),
                padding=ft.padding.symmetric(vertical=15, horizontal=22),
                border=ft.border.all(2, AppColors.SECONDARY),
                border_radius=8,
            ) for digito in codigo_vinculo
        ]
    )

    # Mudamos de ft.View para ft.Container para encaixar no seu layout com a Navbar
    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=40, 
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=40, 
            controls=[
                # Título da Seção
                ft.Text(
                    "Compartilhar Perfil",
                    size=28,
                    weight="bold",
                    color=AppColors.SECONDARY,
                ),
                
                # Mensagem de Instrução
                ft.Text(
                    "Informe o código abaixo para seu cuidador para vincular a conta.\n\n"
                    "Este código é único e expira em 24 horas para sua segurança.",
                    size=16,
                    color=AppColors.SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),

                # As 4 caixinhas do código
                caixinhas_codigo,

                # Botão Copiar
                ft.Container(
                    width=250,
                    height=50,
                    bgcolor=AppColors.TERTIARY,
                    border_radius=8,
                    ink=True, 
                    on_click=copiar_codigo, 
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Copiar Código", color="white", size=18, weight="bold")
                        ]
                    )
                ),
            ]
        )
    )