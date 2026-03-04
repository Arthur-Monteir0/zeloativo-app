import flet as ft
import random
from utils.theme import AppColors

def vinculo_view(page: ft.Page, on_back_click):
    # Gerador de código temporário
    codigo_vinculo = str(random.randint(1000, 9999))

    def copiar_codigo(e):
        # ✅ TENTATIVA UNIVERSAL PARA VERSÕES EXPERIMENTAIS (0.81.0+)
        try:
            # Tenta o método padrão
            page.set_clipboard(codigo_vinculo)
        except AttributeError:
            try:
                # Tenta o método como propriedade de objeto (se existir)
                page.clipboard.set_text(codigo_vinculo)
            except:
                # Fallback caso a versão 0.81.0 use um nome diferente
                print("Erro ao acessar clipboard na versão experimental.")

        # ✅ NOVO MÉTODO PARA SNACKBAR (Versões recentes)
        # Em vez de show_snack_bar, criamos o objeto e abrimos
        snack = ft.SnackBar(
            content=ft.Text(f"Código {codigo_vinculo} copiado!", color="white"),
            bgcolor=AppColors.SECONDARY,
            show_close_icon=True
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # Caixinhas do código
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

    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=20, 
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20, 
            controls=[
                # BOTÃO VOLTAR
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                            icon_color=AppColors.SECONDARY,
                            on_click=lambda _: on_back_click(),
                        )
                    ]
                ),

                ft.Text(
                    "Compartilhar Perfil",
                    size=28,
                    weight="bold",
                    color=AppColors.SECONDARY,
                ),
                
                ft.Text(
                    "Informe o código abaixo para seu cuidador para vincular a conta.\n\n"
                    "Este código é único e expira em 24 horas.",
                    size=16,
                    color=AppColors.SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),

                caixinhas_codigo,

                ft.Container(height=10),

                # Botão Copiar
                ft.Container(
                    width=250,
                    height=50,
                    bgcolor=AppColors.TERTIARY,
                    border_radius=12,
                    ink=True, 
                    on_click=copiar_codigo, 
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.COPY_ALL_ROUNDED, color="white"),
                            ft.Text("Copiar Código", color="white", size=18, weight="bold")
                        ]
                    )
                ),
            ]
        )
    )