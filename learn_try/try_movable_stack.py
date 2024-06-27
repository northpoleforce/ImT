import flet as ft


def main(page: ft.Page):
    card = ft.GestureDetector(
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=70, height=100),
    )

    def drag(dx: int, dy: int):
        card.left += dx
        card.top += dy

    card.on_pan_update = drag

    page.add(ft.Stack(controls=[card], width=1000, height=500))


ft.app(target=main)