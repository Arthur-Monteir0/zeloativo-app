import flet as ft
from utils.theme import AppColors

# ✅ Adicionamos o on_vincular_click aqui
def SharedView(page: ft.Page, on_vincular_click):
    def benefit_card(title, description, icon_name):
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(icon_name, color=AppColors.SECONDARY, size=35),
                title=ft.Text(title, weight="bold", size=18, color=AppColors.SECONDARY),
                subtitle=ft.Text(description, size=16, color=AppColors.SECONDARY),
            ),
            bgcolor="#1A5CC6BA", 
            border_radius=15,
            margin=ft.margin.symmetric(vertical=5),
            padding=5,
        )

    return ft.Container(
        content=ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.PEOPLE_OUTLINE_ROUNDED,
                        color=AppColors.PRIMARY,
                        size=100,
                    ),
                    margin=ft.margin.only(top=20, bottom=10),
                ),
                
                ft.Text(
                    "Cuidado Compartilhado",
                    style=page.theme.text_theme.display_large,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                ft.Text(
                    "Ter um cuidador vinculado garante segurança e autonomia na sua rotina.",
                    style=page.theme.text_theme.body_large,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                ft.Container(height=20),

                benefit_card("Segurança em Dobro", "Seu cuidador é avisado se você esquecer uma dose.", ft.Icons.SHIELD_MOON),
                benefit_card("Apoio na Consulta", "Seu histórico fica disponível para mostrar ao médico.", ft.Icons.ASSIGNMENT_IND),
                benefit_card("Tranquilidade", "Menos peso mental na gestão dos seus remédios.", ft.Icons.FAVORITE),

                ft.Container(height=30),

                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ADD_LINK, color=ft.Colors.WHITE),
                            ft.Text("VINCULAR AGORA", size=20, weight="bold", color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=AppColors.TERTIARY,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                    # ✅ O botão agora chama a função que fará a troca de tela
                    on_click=lambda _: on_vincular_click(), 
                    width=340,
                ),
                
                ft.Text(
                    "Acesse: 'Ajustes > Vincular dependentes' para vincular.",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=AppColors.SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
            ]
        ),
        bgcolor=ft.Colors.WHITE, 
        expand=True,
    )