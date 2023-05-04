import flet as ft


def main(page: ft.Page):
    page.add(ft.Text(value="hello world"))


ft.app(target=main)
