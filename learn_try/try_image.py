import flet as ft

def main(page: ft.Page):
    page.title = "图像示例"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    img = ft.Image(
        src="./concatenated_image_2_20240627060021.png",
        width=100,
        height=100,
        fit=ft.ImageFit.COVER,
    )
    images = ft.Row(expand=1, wrap=False, scroll="always")
    page.add(img, images)
    page.update()

ft.app(target=main)