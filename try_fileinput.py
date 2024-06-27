import flet as ft

def main(page):
    def on_file_selected(e):
        if e.target.files:
            file = e.target.files[0]
            img.src = file.url
            img.update()

    img = ft.Image(width=200, height=200)
    file_input = ft.FileInput(accept="image/*", on_change=on_file_selected)

    page.add(file_input, img)

ft.app(target=main)