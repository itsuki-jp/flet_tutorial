import flet as ft


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.Ref[ft.TextField]()

    def minus_click(e):
        txt_number.current.value = str(int(txt_number.current.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.current.value = str(int(txt_number.current.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                ft.TextField(
                    ref=txt_number, value="0", text_align=ft.TextAlign.RIGHT, width=100
                ),
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)
# ft.app(target=main, view=ft.WEB_BROWSER)
