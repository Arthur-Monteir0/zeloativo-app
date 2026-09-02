import flet as ft
from datetime import date, datetime

from utils.theme import AppColors
from services.data_service import DataService


# ==========================================================
# HELPER — Picker de hora (HH:MM com dropdowns)
# ==========================================================
def hora_picker(label: str, valor_inicial: str = "08:00"):
    partes = (valor_inicial or "08:00").split(":")
    hora_val = partes[0] if partes else "08"
    min_val = partes[1] if len(partes) > 1 else "00"

    dd_hora = ft.Dropdown(
        label="Hora",
        value=hora_val,
        width=100,
        options=[ft.dropdown.Option(f"{h:02d}") for h in range(0, 24)],
    )
    dd_min = ft.Dropdown(
        label="Min",
        value=min_val,
        width=90,
        options=[ft.dropdown.Option(f"{m:02d}") for m in range(0, 60, 5)],
    )

    def get_value():
        return f"{dd_hora.value}:{dd_min.value}"

    row = ft.Column(
        spacing=4,
        controls=[
            ft.Text(label, size=13, color="#666666"),
            ft.Row(spacing=10, controls=[dd_hora, dd_min]),
        ],
    )
    row.get_value = get_value
    return row


# ==========================================================
# HELPER — Picker de data (YYYY-MM-DD com dropdowns)
# ==========================================================
def data_picker(label: str, valor_inicial: str = ""):
    try:
        d = datetime.strptime(valor_inicial, "%Y-%m-%d")
        dia_v, mes_v, ano_v = f"{d.day:02d}", f"{d.month:02d}", str(d.year)
    except Exception:
        hoje = date.today()
        dia_v, mes_v, ano_v = f"{hoje.day:02d}", f"{hoje.month:02d}", str(hoje.year)

    MESES = [
        ("01", "Jan"), ("02", "Fev"), ("03", "Mar"), ("04", "Abr"),
        ("05", "Mai"), ("06", "Jun"), ("07", "Jul"), ("08", "Ago"),
        ("09", "Set"), ("10", "Out"), ("11", "Nov"), ("12", "Dez"),
    ]

    dd_dia = ft.Dropdown(label="Dia", value=dia_v, width=80,
                         options=[ft.dropdown.Option(f"{d:02d}") for d in range(1, 32)])
    dd_mes = ft.Dropdown(label="Mês", value=mes_v, width=100,
                         options=[ft.dropdown.Option(key=k, text=v) for k, v in MESES])
    dd_ano = ft.Dropdown(label="Ano", value=ano_v, width=95,
                         options=[ft.dropdown.Option(str(y)) for y in range(date.today().year, date.today().year + 4)])

    def get_value():
        return f"{dd_ano.value}-{dd_mes.value}-{dd_dia.value}"

    col = ft.Column(
        spacing=4,
        controls=[
            ft.Text(label, size=13, color="#666666"),
            ft.Row(spacing=8, controls=[dd_dia, dd_mes, dd_ano]),
        ],
    )
    col.get_value = get_value
    return col


# ==========================================================
# CARD DE MEDICAMENTO
# ==========================================================
def med_card(page: ft.Page, med: dict, on_edit):
    name = med.get("name") or "Remédio"
    dosage = med.get("dosage") or ""
    label = f"{name} {dosage}".strip()

    return ft.Container(
        padding=20,
        border=ft.border.all(1.5, AppColors.PRIMARY),
        border_radius=20,
        margin=ft.margin.only(bottom=18),
        bgcolor="#FFFFFF",
        shadow=ft.BoxShadow(
            blur_radius=6,
            color=ft.Colors.with_opacity(0.06, "black"),
            offset=ft.Offset(0, 2),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            width=40,
                            height=40,
                            bgcolor="#EEF9F7",
                            border_radius=12,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Icon(ft.Icons.MEDICATION, color=AppColors.PRIMARY, size=22),
                        ),
                        ft.Text(
                            label,
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.SECONDARY,
                        ),
                    ],
                ),
                ft.OutlinedButton(
                    "Editar",
                    icon=ft.Icons.EDIT,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1.5, AppColors.PRIMARY),
                        shape=ft.RoundedRectangleBorder(radius=25),
                        color=AppColors.SECONDARY,
                    ),
                    on_click=lambda e: on_edit(med),
                ),
            ],
        ),
    )


# ==========================================================
# FORM (ADD/EDIT) - BottomSheet
# ==========================================================
def open_form(page: ft.Page, modo: str, refresh_list, med: dict | None = None):
    med = med or {}

    nome = ft.TextField(
        label="Nome do medicamento",
        value=(med.get("name") or "") if modo == "edit" else "",
        border_radius=12,
    )
    dosagem = ft.TextField(
        label="Dosagem (ex: 500mg)",
        value=(med.get("dosage") or "") if modo == "edit" else "",
        border_radius=12,
    )
    observacao = ft.TextField(
        label="Observação / dica de uso",
        value=(med.get("notes") or "") if modo == "edit" else "",
        multiline=True,
        min_lines=2,
        max_lines=3,
        border_radius=12,
    )

    intervalo = ft.Dropdown(
        label="Intervalo entre doses",
        value=str(med.get("interval_hours") or 8) if modo == "edit" else None,
        border_radius=12,
        options=[
            ft.dropdown.Option(key="6",  text="A cada 6 horas"),
            ft.dropdown.Option(key="8",  text="A cada 8 horas"),
            ft.dropdown.Option(key="12", text="A cada 12 horas"),
            ft.dropdown.Option(key="24", text="1x por dia (24h)"),
        ],
    )

    hora_inicio_picker = hora_picker("Horário da 1ª dose", med.get("start_time") or "08:00")
    data_inicio_picker = data_picker("Data de início", med.get("start_date") or "")
    data_fim_picker    = data_picker("Data de término", med.get("end_date") or "")

    def fechar(e=None):
        sheet.open = False
        page.update()

    def show_msg(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
        page.update()

    def salvar(e):
        try:
            payload = {
                "name": nome.value.strip(),
                "dosage": (dosagem.value or "").strip() or None,
                "notes": (observacao.value or "").strip() or None,
                "interval_hours": int(intervalo.value) if intervalo.value else 8,
                "start_date": data_inicio_picker.get_value(),
                "start_time": hora_inicio_picker.get_value(),
                "end_date": data_fim_picker.get_value(),
                "image_url": None,
            }

            if modo == "edit":
                DataService.update_medicine(str(med.get("id")), payload)
                show_msg("Medicamento atualizado ✅")
            else:
                DataService.create_medicine(payload)
                show_msg("Medicamento cadastrado ✅")

            refresh_list()
            fechar()

        except Exception as ex:
            show_msg(f"Erro ao salvar: {ex}")

    def excluir(e):
        try:
            mid = med.get("id")
            if not mid:
                show_msg("ID do medicamento não encontrado.")
                return
            DataService.delete_medicine(str(mid))
            show_msg("Medicamento excluído ✅")
            refresh_list()
            fechar()
        except Exception as ex:
            show_msg(f"Erro ao excluir: {ex}")

    def secao(titulo: str):
        return ft.Container(
            margin=ft.margin.only(top=10, bottom=4),
            content=ft.Text(
                titulo,
                size=14,
                weight=ft.FontWeight.BOLD,
                color=AppColors.SECONDARY,
            ),
        )

    imagem_card = ft.Container(
        height=130,
        bgcolor="#F2F2F2",
        border_radius=15,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.CAMERA_ALT, size=36, color="gray"),
                ft.Text("Toque para adicionar imagem", color="gray", size=13),
            ],
        ),
        on_click=lambda e: show_msg("Upload de imagem: depois a gente liga 👍"),
    )

    botoes = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.ElevatedButton(
                "Salvar",
                expand=True,
                height=55,
                bgcolor=AppColors.PRIMARY,
                color=AppColors.SECONDARY,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=28)),
                on_click=salvar,
            ),
            ft.Container(width=10),
            ft.ElevatedButton(
                "Excluir",
                expand=True,
                height=55,
                bgcolor=AppColors.ALERT,
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=28)),
                visible=(modo == "edit"),
                on_click=excluir,
            ),
        ],
    )

    sheet = ft.BottomSheet(
        content=ft.Container(
            height=page.window_height * 0.95,
            bgcolor="#FFFFFF",
            padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=fechar,
                                icon_color=AppColors.SECONDARY,
                            ),
                            ft.Text(
                                "Editar Medicação" if modo == "edit" else "Adicionar Medicação",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.SECONDARY,
                            ),
                        ],
                    ),
                    imagem_card,

                    secao("📋 Informações do medicamento"),
                    nome,
                    dosagem,
                    observacao,

                    secao("⏱ Agendamento"),
                    intervalo,

                    ft.Container(
                        padding=14,
                        bgcolor="#F8F8F8",
                        border_radius=14,
                        content=ft.Column(
                            spacing=16,
                            controls=[
                                hora_inicio_picker,
                                ft.Divider(height=1, color="#E0E0E0"),
                                data_inicio_picker,
                                ft.Divider(height=1, color="#E0E0E0"),
                                data_fim_picker,
                            ],
                        ),
                    ),

                    ft.Container(height=10),
                    botoes,
                    ft.Container(height=20),
                ],
            ),
        )
    )

    page.overlay.append(sheet)
    sheet.open = True
    page.update()


# ==========================================================
# VIEW PRINCIPAL
# ==========================================================
def meds_view(page: ft.Page):
    page.bgcolor = "#FFFFFF"

    list_col = ft.Column(spacing=0)

    def show_msg(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
        page.update()

    def refresh():
        try:
            list_col.controls.clear()
            meds = DataService.list_medicines() or []
            if not meds:
                list_col.controls.append(
                    ft.Container(
                        padding=16,
                        bgcolor="#F5F5F5",
                        border_radius=16,
                        content=ft.Text(
                            "Nenhum remédio cadastrado ainda 🙂",
                            color=AppColors.SECONDARY,
                        ),
                    )
                )
            else:
                for m in meds:
                    list_col.controls.append(med_card(page, m, on_edit=lambda med: open_form(page, "edit", refresh, med)))
            page.update()
        except Exception as ex:
            show_msg(f"Erro ao carregar: {ex}")

    # init
    refresh()

    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    height=190,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    border_radius=ft.border_radius.only(bottom_left=35, bottom_right=35),
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
                        spacing=0,
                        controls=[
                            ft.Text(
                                "Meus Remédios",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.SECONDARY,
                            ),
                            ft.Text(
                                "Gerencie sua medicação",
                                size=15,
                                color="#888888",
                            ),
                            ft.Container(height=20),

                            list_col,

                            ft.Container(height=20),

                            ft.ElevatedButton(
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(ft.Icons.ADD, color=AppColors.SECONDARY),
                                        ft.Text(
                                            "Adicionar medicação",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=AppColors.SECONDARY,
                                        ),
                                    ],
                                ),
                                width=float("inf"),
                                height=64,
                                bgcolor=AppColors.PRIMARY,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=35),
                                ),
                                on_click=lambda e: open_form(page, "add", refresh, None),
                            ),
                            ft.Container(height=20),
                        ],
                    ),
                ),
            ],
        ),
    )