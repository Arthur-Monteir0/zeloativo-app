import flet as ft
from datetime import date, timedelta
import asyncio
from utils.theme import AppColors
from services.data_service import DataService


DIAS_SEMANA = {0: "SEG", 1: "TER", 2: "QUA", 3: "QUI", 4: "SEX", 5: "SÁB", 6: "DOM"}
MESES_PT = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}
DIAS_SEMANA_FULL = {
    0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
    3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo"
}


def status_color(status: str) -> str:
    s = (status or "pending").lower()
    if s == "taken":
        return AppColors.PRIMARY
    if s == "missed":
        return AppColors.ALERT
    return AppColors.SECONDARY


def status_label(status: str) -> str:
    s = (status or "pending").lower()
    if s == "taken":
        return "Tomado"
    if s == "missed":
        return "Perdido"
    return "Pendente"


def day_selector(page: ft.Page, selected_day: date, on_select_day):
    hoje = date.today()
    days = []
    for delta in range(-2, 5):
        d = hoje + timedelta(days=delta)
        is_selected = d == selected_day

        days.append(
            ft.GestureDetector(
                on_tap=lambda e, d=d: on_select_day(d),  # captura d corretamente
                content=ft.Container(
                    width=52,
                    height=68,
                    border_radius=16,
                    bgcolor=AppColors.PRIMARY if is_selected else "transparent",
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                        controls=[
                            ft.Text(
                                str(d.day),
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.SECONDARY,
                            ),
                            ft.Text(
                                DIAS_SEMANA[d.weekday()],
                                size=11,
                                color=AppColors.SECONDARY if is_selected else "#999999",
                            ),
                        ],
                    ),
                ),
            )
        )

    return ft.Container(
        padding=ft.padding.symmetric(horizontal=4, vertical=8),
        content=ft.Row(scroll=ft.ScrollMode.AUTO, spacing=6, controls=days),
    )


def dose_card(page: ft.Page, item: dict, on_open_detail):
    cor_status = status_color(item.get("status"))
    label_status = status_label(item.get("status"))

    media = ft.Container(
        height=140,
        alignment=ft.Alignment(0, 0),
        content=ft.Icon(ft.Icons.MEDICATION, size=64, color=AppColors.PRIMARY),
    )

    return ft.GestureDetector(
        on_tap=lambda e, it=dict(item): on_open_detail(it),  # snapshot do item
        content=ft.Container(
            width=180,
            padding=12,
            bgcolor="white",
            border_radius=20,
            border=ft.border.all(1.5, "#E0E0E0"),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Container(bgcolor="#F5FAFA", border_radius=14, content=media),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                bgcolor=AppColors.SECONDARY,
                                border_radius=20,
                                content=ft.Text(
                                    item.get("time", "--:--"),
                                    color="white",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                bgcolor=cor_status,
                                border_radius=20,
                                content=ft.Text(
                                    label_status,
                                    color="white",
                                    size=11,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                        ],
                    ),
                    ft.Text(
                        item.get("medicine_name") or "Remédio",
                        size=13,
                        weight=ft.FontWeight.W_600,
                        color=AppColors.SECONDARY,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
            ),
        ),
    )


def open_dose_detail(page: ft.Page, item: dict, on_taken, on_refresh):
    def show_msg(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
        page.update()

    def fechar(e=None):
        try:
            sheet.open = False
            if sheet in page.overlay:
                page.overlay.remove(sheet)
        except Exception:
            pass
        page.update()

    def marcar_tomado(e=None):
        # impede marcar de novo
        if (item.get("status") or "").lower() == "taken":
            show_msg("Essa dose já está como tomada ✅")
            return
        on_taken(str(item.get("id")))
        fechar()

    # (por enquanto) só simula o adiar
    def adiar(minutos: int):
        def _adiar(e=None):
            try:
                event_id = str(item.get("id"))
                resp = DataService.snooze_intake(event_id, minutes=minutos)
                # se o backend devolver erro em {"detail": "..."}
                if isinstance(resp, dict) and resp.get("detail"):
                    show_msg(f"Erro ao adiar: {resp['detail']}")
                    return

                show_msg(f"Adiado {minutos} min ✅")
                on_refresh()   # ✅ recarrega a home
                fechar()
            except Exception as ex:
                show_msg(f"Erro ao adiar: {ex}")
        return _adiar

    botoes_adiar_container = ft.Container(
        visible=False,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.OutlinedButton(
                    "⏱ 15 min",
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1.5, AppColors.SECONDARY),
                        shape=ft.RoundedRectangleBorder(radius=20),
                        color=AppColors.SECONDARY,
                    ),
                    on_click=adiar(15),
                ),
                ft.OutlinedButton(
                    "⏱ 1 hora",
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1.5, AppColors.SECONDARY),
                        shape=ft.RoundedRectangleBorder(radius=20),
                        color=AppColors.SECONDARY,
                    ),
                    on_click=adiar(60),
                ),
            ],
        ),
    )

    def toggle_adiar(e=None):
        botoes_adiar_container.visible = not botoes_adiar_container.visible
        page.update()

    # topo (imagem/ícone)
    foto_card = ft.Stack(
        controls=[
            ft.Container(
                height=260,
                bgcolor="#EEF6F5",
                border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.MEDICATION, size=80, color=AppColors.PRIMARY),
                        ft.Text(
                            item.get("medicine_name") or "Remédio",
                            size=15,
                            color=AppColors.SECONDARY,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),
            ),
            ft.Container(
                top=12,
                left=12,
                content=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    icon_color=AppColors.SECONDARY,
                    bgcolor="white",
                    on_click=fechar,
                ),
            ),
        ],
    )

    sheet_content = ft.Container(
        height=page.window_height * 0.90,
        bgcolor="#FFFFFF",
        padding=0,
        content=ft.Column(
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                foto_card,
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=24, vertical=20),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Text(
                                item.get("medicine_name") or "Remédio",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.SECONDARY,
                            ),
                            ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Text("⏳", size=18),
                                    ft.Text(
                                        f"Horário: {item.get('time','--:--')}",
                                        size=18,
                                        color=AppColors.SECONDARY,
                                    ),
                                ],
                            ),
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                bgcolor=status_color(item.get("status")),
                                border_radius=20,
                                content=ft.Text(
                                    status_label(item.get("status")),
                                    color="white",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Container(height=10),

                            ft.ElevatedButton(
                                "Tomei o Remédio",
                                width=float("inf"),
                                height=58,
                                bgcolor=AppColors.PRIMARY,
                                color=AppColors.SECONDARY,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=30),
                                    text_style=ft.TextStyle(size=17, weight=ft.FontWeight.BOLD),
                                ),
                                on_click=marcar_tomado,
                            ),

                            ft.ElevatedButton(
                                "Adiar",
                                width=float("inf"),
                                height=52,
                                bgcolor=AppColors.SECONDARY,
                                color="white",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                                on_click=toggle_adiar,
                            ),
                            botoes_adiar_container,

                            ft.Container(height=12),
                        ],
                    ),
                ),
            ],
        ),
    )

    sheet = ft.BottomSheet(content=sheet_content)
    page.overlay.append(sheet)
    sheet.open = True
    page.update()


def home_view(page: ft.Page):
    selected_day = date.today()
    items: list[dict] = []

    def show_msg(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
        page.update()

    # Textos dinâmicos dos contadores
    txt_tomadas = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, color=AppColors.PRIMARY)
    txt_pendentes = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY)
    txt_perdidas = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, color=AppColors.ALERT)

    # Containers que vamos atualizar
    lista_container = ft.Container()
    selector_container = ft.Container()

    def load_day(d: date):
        nonlocal items
        try:
            res = DataService.get_day_history(d.isoformat(), tz_offset_hours=-3)

            # se veio erro:
            if isinstance(res, dict) and res.get("detail"):
                items = []
                show_msg(f"Erro: {res['detail']}")
                return

            events = (res.get("items") if isinstance(res, dict) else []) or []
            items = []
            for ev in events:
                items.append(
                    {
                        "id": str(ev.get("id")),
                        "medicine_name": ev.get("medicine_name") or "Remédio",
                        "time": ev.get("time") or "--:--",
                        "status": (ev.get("status") or "pending").lower(),
                    }
                )
        except Exception as ex:
            items = []
            show_msg(f"Erro ao carregar doses: {ex}")

    def rebuild():
        # lista de cards
        cards = []
        for it in items:
            it_snap = dict(it)
            cards.append(dose_card(page, it_snap, on_open_detail=open_detail))

        if not cards:
            lista_container.content = ft.Row(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        padding=16,
                        bgcolor="#F5F5F5",
                        border_radius=16,
                        content=ft.Text("Nenhuma dose nesse dia 🙂", color=AppColors.SECONDARY),
                    )
                ],
            )
        else:
            lista_container.content = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=14, controls=cards)

        # contadores
        tomadas = sum(1 for it in items if (it.get("status") or "").lower() == "taken")
        pendentes = sum(1 for it in items if (it.get("status") or "").lower() == "pending")
        perdidas = sum(1 for it in items if (it.get("status") or "").lower() == "missed")

        txt_tomadas.value = str(tomadas)
        txt_pendentes.value = str(pendentes)
        txt_perdidas.value = str(perdidas)

        page.update()

    def refresh_home():
        load_day(selected_day)
        rebuild()

    def on_taken(event_id: str):
        try:
            resp = DataService.update_intake_status(str(event_id), "taken")

            # erro em JSON
            if isinstance(resp, dict) and resp.get("detail"):
                show_msg(f"Erro: {resp['detail']}")
                return

            # atualiza localmente pra mudar na hora
            for it in items:
                if str(it.get("id")) == str(event_id):
                    it["status"] = "taken"
                    break

            refresh_home()
            show_msg("Marcado como tomado ✅")

        except Exception as ex:
            show_msg(f"Erro ao marcar como tomado: {ex}")

    def open_detail(item: dict):
        open_dose_detail(page, item, on_taken, refresh_home)

    def on_select_day(d: date):
        nonlocal selected_day
        selected_day = d
        load_day(selected_day)

        # refaz seletor com o dia selecionado pintado
        selector_container.content = day_selector(page, selected_day, on_select_day)
        rebuild()

    # init
    load_day(selected_day)
    selector_container.content = day_selector(page, selected_day, on_select_day)
    rebuild()

    hoje = date.today()
    dia_semana_full = DIAS_SEMANA_FULL[hoje.weekday()]
    data_formatada = f"{dia_semana_full}, {hoje.day} de {MESES_PT[hoje.month]}"

    async def auto_refresh():
        while True:
            await asyncio.sleep(5)  # atualiza a cada 5 segundos
            refresh_home()
    page.run_task(auto_refresh)
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.padding.only(left=4, bottom=6),
                content=ft.Text(
                    data_formatada,
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=AppColors.SECONDARY,
                ),
            ),

            selector_container,
            ft.Container(height=16),

            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        "Próximas Doses",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.SECONDARY,
                    ),
                    ft.TextButton("Ver todas", style=ft.ButtonStyle(color=AppColors.PRIMARY)),
                ],
            ),

            ft.Container(height=10),
            lista_container,
            ft.Container(height=20),

            ft.Container(
                padding=16,
                bgcolor="#EEF9F7",
                border_radius=16,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            controls=[
                                ft.Text("✅", size=24),
                                txt_tomadas,
                                ft.Text("Tomadas", size=12, color=AppColors.SECONDARY),
                            ],
                        ),
                        ft.VerticalDivider(color="#CCCCCC", width=1),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            controls=[
                                ft.Text("⏳", size=24),
                                txt_pendentes,
                                ft.Text("Pendentes", size=12, color=AppColors.SECONDARY),
                            ],
                        ),
                        ft.VerticalDivider(color="#CCCCCC", width=1),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            controls=[
                                ft.Text("🔴", size=24),
                                txt_perdidas,
                                ft.Text("Perdidas", size=12, color=AppColors.SECONDARY),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )