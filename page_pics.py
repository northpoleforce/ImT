import flet as ft
from PIL import Image as PILImage

files_path = []  # 全局变量，用于存储选中文件的路径列表

# draggable_list = []  # 用于存储创建的 Draggable 对象
# dragtarget_list = []  # 用于存储创建的 DragTarget 对象

def main(page: ft.Page):
    draggable_list = []  # 用于存储创建的 Draggable 对象
    dragtarget_list = []  # 用于存储创建的 DragTarget 对象
    # draggable_row = ft.Row(scroll=ft.ScrollMode.ALWAYS)
    # dragtarget_row = ft.Row(scroll=ft.ScrollMode.ALWAYS)
    draggable_column = ft.Column(scroll=ft.ScrollMode.ALWAYS)    # draggablez组件
    dragtarget_column = ft.Column(scroll=ft.ScrollMode.ALWAYS)   # dragtarget组件

    def pick_files_result(e: ft.FilePickerResultEvent):
        global files_path  # 使用全局变量
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "已取消！"
        )
        # files_path是一个列表，装有所有选中文件的路径
        files_path = list(map(lambda f: f.path, e.files))

        def drag_will_accept(e):
            # 这是一个回调函数，当一个Draggable对象被拖动到一个DragTarget对象上时，会调用这个函数
            e.control.content.border = ft.border.all(
                2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
            )  # 如果e.data为"true"，则边框颜色为黑色，否则为红色， e.data是Draggable对象的data属性
            e.control.update()

        def drag_accept(e: ft.DragTargetAcceptEvent):
            src = page.get_control(e.src_id)
            e.control.content.bgcolor = src.content.bgcolor
            e.control.content.border = None
            e.control.content.content.src = src.content.content.src
            e.control.update()

        def drag_leave(e):
            e.control.content.border = None
            e.control.update()

        # 使用for循环创建n个Draggable对象，添加到列表中
        # draggable_list = []
        # dragtarget_list = []
        for img_path in files_path:
            draggable = ft.Draggable(
                group="photo",
                content=ft.Container(
                    content=ft.Image(
                        src=img_path,
                        width=100,
                        height=100,
                        fit=ft.ImageFit.CONTAIN,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                )
            )
            draggable_list.append(draggable)
            draggable_column.controls.append(draggable)

            dragtarget = ft.DragTarget(
                group="photo",
                content=ft.Container(
                    content=ft.Image(
                        src=" ",
                        width=100,
                        height=100,
                        fit=ft.ImageFit.CONTAIN,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                    bgcolor=ft.colors.BLUE_GREY_100,
                    border_radius=5,
                ),
                on_will_accept=drag_will_accept,
                on_accept=drag_accept,
                on_leave=drag_leave,
            )
            dragtarget_list.append(dragtarget)
            dragtarget_column.controls.append(dragtarget)

        # page.add(
        #     ft.Row(
        #         [
        #             ft.Column(
        #                 draggable_list,
        #                 expand=len(files_path), scroll=ft.ScrollMode.ALWAYS
        #             ),
        #             ft.Column(
        #                 dragtarget_list,
        #                 expand=len(files_path), scroll=ft.ScrollMode.ALWAYS
        #             ),
        #         ]
        #     )
        # )
        selected_files.update()
        page.update()

    def concatenate_images():
        nonlocal dragtarget_list    # 使用全局变量

        if not dragtarget_list:
            print("没有选择文件或没有完成拖放操作")
            return

        print("已选择文件：")
        print([target.content.content.src for target in dragtarget_list])

        # 获取所有图片，并调整大小为第一张图片的大小
        images = []
        base_width, base_height = PILImage.open(dragtarget_list[0].content.content.src).size
        for target in dragtarget_list:
            img_path = target.content.content.src
            img = PILImage.open(img_path)
            resized_img = img.resize((base_width, base_height))
            images.append(resized_img)

        # 拼接图片示例：根据奇偶数量处理
        if len(images) % 2 == 0:  # 如果是偶数张图片
            # 添加一张白色的空白图片
            blank_image = PILImage.new('RGB', (images[0].width, images[0].height), (0, 0, 0))
            images.append(blank_image)

        # 计算拼接后图片的尺寸
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)
        new_image = PILImage.new('RGB', (max_width, total_height))

        # 拼接图片
        y_offset = 0
        for img in images:
            new_image.paste(img, (0, y_offset))
            y_offset += img.height


        print("垂直拼接成功\r\n")

        # 将拼接后的图片保存到临时文件路径
        new_image_path = "concatenated_image.png"
        new_image.save(new_image_path)

        # 更新界面上的图片显示
        img_widget.src = new_image_path
        img_widget.update()

        print(f"拼接后的图片已保存到 {new_image_path}")


    def save_concatenated_image():
        nonlocal img_widget

        # 获取当前显示的拼接图片
        if img_widget.src:
            try:
                # 打开图片文件
                img = PILImage.open(img_widget.src)

                # 保存图片到新路径
                new_image_path = "final_image.png"
                img.save(new_image_path)
                print(f"拼接后的图片已保存到 {new_image_path}")

            except IOError as e:
                print(f"无法打开或保存图片：{e}")
        else:
            print("当前没有有效的图片路径")

    def clear_all():
        # 清空拖拽相关列表和控件
        draggable_column.controls.clear()
        dragtarget_column.controls.clear()
        draggable_list.clear()
        dragtarget_list.clear()

        # 移除图片控件
        #page.remove(img_widget)
        page.update()   # 更新页面

    page.title = "第x张长图"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50  # 50px的内边距

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    img_widget = ft.Image(src=" ", width=400, height=300, fit=ft.ImageFit.CONTAIN)

    # grids = ft.GridView(  # 创建一个网格视图
    #         expand=1,  # 设置网格视图占满整个页面
    #         runs_count=3,
    #         max_extent=150,  # 设置图片最大尺寸为150
    #         child_aspect_ratio=1.0,  # 设置图片宽高比为1
    #         spacing=[3,3],  # 设置图片间距为5
    #         run_spacing=5,  # 设置行间距为5
    #         # spacing=5,
    #     )
    # page.add(grids)
    # for i in range(9):
    #     grids.controls.append(
    #         ft.Container(
    #             width=500,
    #             height=500,
    #             bgcolor=ft.colors.GREEN,
    #             border_radius=5,
    #         )
    # main_column_list = []
    # main_row = ft.Row(
    #     [
    #         ft.Column(
    #         )
    #         ]
    # )

    # 创建3个Row对象，每个Row对象包含3个Container对象
    rows = []
    for _ in range(3):
        row = ft.Row()
        for _ in range(3):
            container = ft.Container(
                width=150,
                height=150,
                bgcolor=ft.colors.GREEN,
                border_radius=5,
            )
            row.controls.append(container)
        rows.append(row)
    # 创建一个Column对象，包含3个Row对象
    column = ft.Column()
    for row in rows:
        column.controls.append(row)
    page.add(column)

            # ft.Image(
            #     src=f"https://picsum.photos/150/150?{i}",
            #     fit=ft.ImageFit.NONE,
            #     repeat=ft.ImageRepeat.NO_REPEAT,
            #     border_radius=ft.border_radius.all(10),
            # )

    # page.overlay.append(pick_files_dialog)
    # page.add(
    #     ft.Row(
    #         [
    #             ft.ElevatedButton(  # 创建一个按钮，点击后弹出文件选择对话框
    #                 "选择文件",
    #                 icon=ft.icons.UPLOAD_FILE,
    #                 on_click=lambda _: pick_files_dialog.pick_files(
    #                     allow_multiple=True,
    #                     allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp"]
    #                 ),
    #             ),
    #             selected_files,
    #         ]
    #     ),
    #     ft.Row(
    #         [
    #             ft.ElevatedButton(  # 创建一个按钮，点击后拼接图片
    #                 "拼接图片",
    #                 on_click=lambda _: concatenate_images(),
    #             ),
    #             ft.ElevatedButton(  # 创建一个按钮，点击后保存拼接图片
    #                 "保存拼接图片",
    #                 on_click=lambda _: save_concatenated_image(),
    #             ),
    #             ft.ElevatedButton(  # 创建一个按钮，点击后清除所有图片
    #                 "清除",
    #                 on_click=lambda _: clear_all(),
    #             ),
    #         ]
    #     ),
    #     ft.Row(
    #         [
    #             draggable_column,   # 拖拽图片的列
    #             dragtarget_column,  # 拖拽目标的列
    #             img_widget,        # 显示拼接后的图片
    #         ]
    #     ),
    # )
    page.update()


ft.app(target=main)
