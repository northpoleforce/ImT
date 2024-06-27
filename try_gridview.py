import flet as ft

def main(page: ft.Page):
    page.title = "GridView 示例"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.update()

    images = ft.GridView(   # 创建一个网格视图
        expand=1,   # 设置网格视图占满整个页面
        runs_count=5,   # 设置每行显示5个图片
        max_extent=150,  # 设置图片最大尺寸为150
        child_aspect_ratio=1.0,  # 设置图片宽高比为1
        spacing=5,  # 设置图片间距为5
        run_spacing=5,  # 设置行间距为5
    )

    page.add(images)

    for i in range(0, 60):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/150/150?{i}",
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)