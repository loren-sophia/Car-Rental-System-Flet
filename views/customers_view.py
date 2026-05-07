import flet as ft
import re
from database.customer_queries import (
    get_all_customers, add_customer, update_customer, delete_customer
)
from utils.theme import (
    BG, PRIMARY, SUCCESS, WARNING, DANGER,
    CARD_BG, CARD_SEL, HEADER_BG, BORDER_COL,
    TEXT_DARK, TEXT_LIGHT, TEXT_GREY, TEXT_MUTED,
    section_title, primary_btn, danger_btn, mk_field,
    tbl_header, snack, confirm_dialog,
    open_dialog, close_dialog
)

COLS   = ["ID", "Nombre",   "Teléfono",  "Email",   "Licencia"]
WIDTHS = [45,   180,         130,          200,        150]


def customers_view(page: ft.Page) -> ft.Container:
    selected   = {"data": None}
    search_fld = mk_field("Buscar por nombre, teléfono, email o licencia...", width=420)
    table_body = ft.Column(spacing=1, scroll=ft.ScrollMode.AUTO, expand=True)

    def make_row(c):
        is_sel = selected["data"] and selected["data"]["id"] == c["id"]
        def on_click(e): selected["data"] = c; load()
        return ft.Container(
            content=ft.Row([
                ft.Text(str(c["id"]),        width=WIDTHS[0], size=12, color=TEXT_GREY),
                ft.Text(c["full_name"],      width=WIDTHS[1], size=12, color=TEXT_DARK, weight="bold"),
                ft.Text(c["phone"],          width=WIDTHS[2], size=12, color=TEXT_GREY),
                ft.Text(c["email"] or "—",   width=WIDTHS[3], size=12, color=TEXT_MUTED),
                ft.Text(c["license_number"], width=WIDTHS[4], size=12, color=TEXT_GREY),
            ]),
            bgcolor=CARD_SEL if is_sel else CARD_BG,
            border_radius=6,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            on_click=on_click, ink=True,
            border=ft.border.all(1, PRIMARY if is_sel else BORDER_COL),
        )

    def load(e=None):
        s = search_fld.value.strip() if search_fld.value else None
        table_body.controls = [make_row(c) for c in get_all_customers(s or None)]
        page.update()

    def clear_search(e):
        search_fld.value = ""; selected["data"] = None; load()

    def open_form(customer=None):
        ie = customer is not None
        f_name  = mk_field("Nombre completo *", customer["full_name"]      if ie else "", width=340)
        f_phone = mk_field("Teléfono *",        customer["phone"]          if ie else "", width=200)
        f_email = mk_field("Email (opcional)",  customer["email"] or ""    if ie else "", width=280)
        f_lic   = mk_field("No. Licencia *",    customer["license_number"] if ie else "", width=200)
        err     = ft.Text("", color=DANGER, size=12)

        def save(e):
            name  = f_name.value.strip()  if f_name.value  else ""
            phone = f_phone.value.strip() if f_phone.value else ""
            email = f_email.value.strip() if f_email.value else ""
            lic   = f_lic.value.strip()   if f_lic.value   else ""

            if not name:
                err.value = "⚠ El nombre es obligatorio."; page.update(); return
            if not phone:
                err.value = "⚠ El teléfono es obligatorio."; page.update(); return
            if not lic:
                err.value = "⚠ El número de licencia es obligatorio."; page.update(); return
            if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
                err.value = "⚠ El email no tiene un formato válido."; page.update(); return

            if ie:
                ok, msg = update_customer(customer["id"], name, phone, email, lic)
            else:
                ok, msg = add_customer(name, phone, email, lic)

            if ok:
                close_dialog(page, dlg)
                snack(page, msg)
                selected["data"] = None
                load()
            else:
                err.value = f"⚠ {msg}"; page.update()

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=CARD_BG,
            title=ft.Text("✏️ Editar Cliente" if ie else "➕ Nuevo Cliente", color=TEXT_DARK, size=16),
            content=ft.Container(
                bgcolor=CARD_BG,
                width=460,
                height=300,
                content=ft.Column([
                    f_name,
                    ft.Row([f_phone, f_email], spacing=12),
                    f_lic,
                    err,
                ], spacing=14, tight=True),
            ),
            actions=[
                ft.ElevatedButton("💾 Guardar", on_click=save, bgcolor=SUCCESS, color=TEXT_LIGHT),
                ft.ElevatedButton("Cancelar",   on_click=lambda e: close_dialog(page, dlg),
                                  bgcolor=HEADER_BG, color=TEXT_MUTED),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        open_dialog(page, dlg)

    def edit(e):
        if not selected["data"]:
            snack(page, "Selecciona un cliente de la tabla primero.", error=True); return
        open_form(selected["data"])

    def delete(e):
        if not selected["data"]:
            snack(page, "Selecciona un cliente de la tabla primero.", error=True); return
        c = selected["data"]
        def do():
            ok, msg = delete_customer(c["id"])
            snack(page, msg, error=not ok)
            if ok: selected["data"] = None; load()
        confirm_dialog(page, f"¿Eliminar al cliente {c['full_name']}?", do)

    load()

    return ft.Container(
        content=ft.Column([
            ft.Row([section_title("👥 Clientes")]),
            ft.Divider(height=1, color=BORDER_COL),
            ft.Row([search_fld,
                    primary_btn("🔍 Buscar", load),
                    ft.ElevatedButton("Limpiar", on_click=clear_search,
                                      bgcolor=HEADER_BG, color=TEXT_MUTED)],
                   spacing=8),
            ft.Row([primary_btn("➕ Agregar", lambda e: open_form(), SUCCESS),
                    primary_btn("✏️ Editar",  edit, WARNING),
                    danger_btn("🗑 Eliminar",  delete)], spacing=8),
            tbl_header(COLS, WIDTHS),
            ft.Container(
                content=table_body, expand=True, bgcolor=CARD_BG,
                border=ft.border.all(1, BORDER_COL),
                border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
            ),
        ], spacing=12, expand=True),
        bgcolor=BG, padding=24, expand=True,
    )
