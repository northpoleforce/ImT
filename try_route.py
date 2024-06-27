import flet as ft

def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change(route):
        page.views.clear()  # Clear all views
        page.views.append(  # Add home view
            ft.View(
                "/",
                [
                    # Add an app bar with a title
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    # Add a button to visit the store
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)