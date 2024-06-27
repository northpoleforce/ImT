import flet as ft

def main(page: ft.Page):
    page.title = "主页面"

    def open_new_page(_):
        new_page = ft.Page()
        new_page.title = "新页面"
        new_page.add(ft.Text("这是一个新的页面"))
        page.navigate(new_page)

    container = ft.Container(
        width=150,
        height=150,
        bgcolor=ft.colors.GREEN,
        border_radius=5,
        on_click=open_new_page,
    )

    page.add(container)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)