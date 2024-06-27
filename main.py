import os
import datetime

import flet as ft

from PIL import Image as pimg


def pic_stitch(pic_id, dragtarget_column):
    print("pic_stitch")
    print(len(dragtarget_column.controls))
    images = []
    max_width = 0
    max_height = 0
    i = 0
    h1 = 0
    h2 = 0
    mid = len(dragtarget_column.controls) // 2
    for control in dragtarget_column.controls:
        print(control.content.content.src)
        img = pimg.open(control.content.content.src)
        images.append(img)
        max_width = max(max_width, img.width)
        max_height = max(max_height, img.height)
        if i < mid:
            h1 += img.height
        elif i > mid:
            h2 += img.height
        i += 1
    if h1 > h2:
        blank_image = pimg.new('RGB', (max_width, h1-h2), (0, 0, 0))
        images.append(blank_image)
    elif h1 < h2:
        blank_image = pimg.new('RGB', (max_width, h2-h1), (0, 0, 0))
        images.insert(0, blank_image)
    # if len(images)%2 == 0:
    #     blank_image = pimg.new('RGB', (max_width, max_height), (0, 0, 0))
    #     images.append(blank_image)
    total_height = sum(img.height for img in images)
    new_image = pimg.new('RGB', (max_width, total_height))
    y_offset = 0
    for img in images:
        x_offset = (max_width - img.width) // 2  # 计算x坐标
        new_image.paste(img, (x_offset, y_offset))
        # new_image.paste(img, (0, y_offset))
        y_offset += img.height
    # new_image_path = f"concatenated_image_{pic_id}.png"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_image_path = f"concatenated_image_{pic_id}_{timestamp}.png"
    new_image.save(new_image_path)
    return new_image_path


def main(page: ft.Page):
    page.title = "为朋友圈发长图而生"

    main_column = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        spacing=2,
    )
    main_containers = []

    def init():
        nonlocal main_containers

        def create_on_click_handler(i):
            return lambda _: page.go(f"/long_pic_{i}")

        main_containers = [
            ft.Container(
                content=ft.Image(
                    src=" ",
                    tooltip=f"长图{i + 1}",
                    fit=ft.ImageFit.COVER,
                    width=300,
                    height=300,
                ),
                width=150,
                height=150,
                bgcolor=ft.colors.GREEN,
                # border_radius=5,
                image_fit=ft.ImageFit.COVER,
                ink=True,
                ink_color=ft.colors.BLUE,
                # padding=ft.padding.symmetric(horizontal=0),

                on_click=create_on_click_handler(i + 1),
            )
            for i in range(9)
        ]
        rows = [ft.Row(
            spacing=2,
            scroll=ft.ScrollMode.ALWAYS,
        ) for _ in range(3)]
        for i in range(9):
            rows[i // 3].controls.append(main_containers[i])
        main_column.controls.extend(rows)

    def remove_home(controls):
        for control in controls:
            if isinstance(control, ft.ElevatedButton):
                controls.remove(control)

    def remove_image_and_home(controls):
        for control in controls:
            if isinstance(control, ft.Image):
                os.remove(control.src)
                controls.remove(control)
        remove_home(controls)

    def remove_column_and_home(controls):
        for control in controls:
            if isinstance(control, ft.Column):
                controls.remove(control)
        remove_home(controls)

    # def remove_column_and_home(controls):
    #     controls[:] = [control for control in controls if
    #                    not isinstance(control, (ft.Column, ft.ElevatedButton))]

    def pic_edit(controls, col):
        print("edit")
        remove_image_and_home(controls)
        controls.append(col)
        controls.append(ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")), )

    def pic_preview(controls, pic_id):
        print("preview")
        drag_row = controls[-2].controls[-1]
        print(controls)
        print(drag_row)
        main_containers[pic_id - 1].content.src = pic_stitch(pic_id, drag_row.controls[1])
        remove_column_and_home(controls)
        controls.append(
            ft.Image(
                src=main_containers[pic_id - 1].content.src,
                width=400,
                height=400,
            )
        )
        controls.append(ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),)

    def pic_preview_ready(controls, pic_id):
        print("preview_ready")
        print(main_containers[pic_id - 1].content.src)
        remove_column_and_home(controls)
        controls.append(
            ft.Image(
                src=main_containers[pic_id - 1].content.src,
                width=400,
                height=400,
            )
        )
        controls.append(ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")), )

    def pic_save(controls, pic_id):
        print("save")
        drag_row = controls[-2].controls[-1]
        print(controls)
        print(drag_row)
        main_containers[pic_id - 1].content.src = pic_stitch(pic_id, drag_row.controls[1])

    def route_change(route):
        page.views.clear()  # Clear all views
        page.views.append(  # Add home view
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("朋友圈长图总体预览"), bgcolor=ft.colors.SURFACE_VARIANT),
                    main_column,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS,
                auto_scroll=True,
            )
        )
        page.update()

        draggable_column = ft.Column()
        dragtarget_column = ft.Column()

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

        def pick_files_result(e: ft.FilePickerResultEvent):
            # nonlocal images_path
            images_path = list(map(lambda f: f.path, e.files))
            # original_images.controls.clear()
            draggable_column.controls.clear()
            dragtarget_column.controls.clear()
            n = len(images_path)
            for i in range(n):
            # for img_path in images_path:
                # original_images.controls.append(
                draggable_column.controls.append(
                    ft.Draggable(
                        group="photo",
                        content=ft.Container(
                            content=ft.Image(
                                src=images_path[i],
                                width=100,
                                height=100,
                                fit=ft.ImageFit.CONTAIN,
                                repeat=ft.ImageRepeat.NO_REPEAT,
                                border_radius=ft.border_radius.all(10),
                            ),
                            bgcolor=ft.colors.BLUE_GREY_100,
                            border_radius=5,
                        ),
                    )
                )
                w = 100
                h = 100
                if i == n//2:
                    w = 125
                    h = 125
                dragtarget_column.controls.append(
                    ft.DragTarget(
                        group="photo",
                        content=ft.Container(
                            content=ft.Image(
                                src=" ",
                                width=w,
                                height=h,
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
                )
            page.update()

        pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        upload_button = ft.ElevatedButton(  # 创建一个按钮，点击后弹出图片选择对话框
            "上传图片",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=True,
                allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp"]
            ),
        )
        def create_on_click_handler():
            # return lambda _: pic_save(page.views[-1].controls, int(page.route.split("_")[-1]))
            def on_click(_):
                print("save")
                # now_view = page.views[-1]
                # drag_row = now_view.controls[-2].controls[-1]
                # print(page.views[-1].controls)
                # print(drag_row)
                main_containers[pic_index - 1].content.src = pic_stitch(pic_index - 1, drag_row.controls[1])
                print(main_containers[pic_index - 1].content.src)
            return on_click
        save_button = ft.ElevatedButton(
            "保存长图",
            icon=ft.icons.SAVE,
            on_click=create_on_click_handler(),
        )

        col = ft.Column()
        drag_row = ft.Row([draggable_column, dragtarget_column])

        def change_status(pic_id):
            def change_content(e):
                nav_dest = e.control.selected_index
                now_view = page.views[-1]

                if nav_dest == 0:
                    # print("edit")
                    # remove_image(now_view)
                    # now_view.controls.append(col)
                    pic_edit(now_view.controls, col)
                else:
                    # print("preview")
                    # remove_column(now_view)
                    # main_containers[pic_id - 1].content.src = pic_stitch(pic_id, drag_row.controls[1])
                    # now_view.controls.append(
                    #     ft.Image(
                    #         src=main_containers[pic_id - 1].content.src,
                    #     )
                    # )
                    pic_preview(now_view.controls, pic_id)
                page.update()
            return change_content

        if page.route.startswith("/long_pic_"):
            print(page.route)

            def load_sub_page():
                # print("unload", col.controls)
                col.controls = [
                    pick_files_dialog,
                    upload_button,
                    save_button,
                    drag_row,
                ]

            load_sub_page()
            pic_index = int(page.route.split("_")[-1])
            page.views.append(
                ft.View(
                    page.route,
                    [
                        ft.AppBar(title=ft.Text(f"长图{pic_index}"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.NavigationBar(
                            destinations=[
                                ft.NavigationBarDestination(
                                    icon=ft.icons.EXPLORE, label="编辑",
                                ),
                                ft.NavigationBarDestination(
                                    icon=ft.icons.COMMUTE, label="预览",
                                ),
                            ],
                            on_change=change_status(pic_index),
                        ),
                        col,
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
            if main_containers[pic_index - 1].content.src != " ":  # 如果已经拼接过长图
                pic_preview_ready(page.views[-1].controls, pic_index)
            page.update()
        page.update()

    # def sub_back_to_home(now_view):
    #     print("back", now_view)
    #     # now_view = page.views[-1]
    #     if isinstance(now_view.controls[-1], ft.ElevatedButton):
    #         if isinstance(now_view.controls[-2], ft.Column):
    #             pic_preview(now_view, int(now_view.route.split("_")[-1]))

    def view_pop(view):
        # page.update()
        # sub_back_to_home(view)
        page.views.pop()
        page.update()
        top_view = page.views[-1]
        page.go(top_view.route)

    init()
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    print(page.route)
    page.go(page.route)


ft.app(target=main)
