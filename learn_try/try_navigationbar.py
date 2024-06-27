import flet as ft

def main(page: ft.Page):

    page.title = "导航栏示例"
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="探索"),
            ft.NavigationDestination(icon=ft.icons.COMMUTE, label="通勤"),
            ft.NavigationDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="探索",
            ),
        ]
    )
    page.add(ft.Text("正文！"))

ft.app(target=main)