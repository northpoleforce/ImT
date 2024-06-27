import flet as ft
import numpy as np
import cv2

from PIL import Image

import image_compression as ic
import beautify as bt


# 用PIL读取图像，然后转换为OpenCV格式（因为imread函数无法读取中文路径，PIL可以）
def read_image(image_path):
    # 使用PIL库读取图像
    pil_image = Image.open(image_path)
    # 将PIL图像转换为NumPy数组
    numpy_image = np.array(pil_image)
    # 由于PIL和OpenCV的颜色通道顺序不同，需要将RGB转换为BGR
    numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    return numpy_image


def main(page: ft.Page):
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "已取消！"
        )
        selected_files.update()
        img_origin.src = next(map(lambda f: f.path, e.files))
        page.update()
        # print(img_origin.src)
        # ic.compress_image(img_origin.src.replace("\\", "\\\\"), "compressed_image.jpg", quality=20)
        # read_image(img_origin.src)
        # ic.compress_image(read_image(img_origin.src), "compressed_image.jpg", quality=20)
        # ic.compress_image(r"图像压缩\image1.jpg", "compressed_image.jpg", quality=20)
        # img_result.src = "compressed_image.jpg"

    # ic.compress_image("图像压缩\\\\image1.jpg", "compressed_image.jpg", quality=20)
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)  # 这是一个文件选择对话框
    selected_files = ft.Text()
    # img = ft.Image(src=" ", width=500, height=500)
    img_origin = ft.Image(src=" ", width=300, height=300)
    img_result = ft.Image(src=" ", width=300, height=300)

    def img_compress(e):
        ic.compress_image(read_image(img_origin.src), "compressed_image.jpg", quality=20)
        img_result.src = "compressed_image.jpg"
        page.update()

    def img_beauty(e):
        bt.apply_beauty_filter(read_image(img_origin.src))
        img_result.src = "beautified_image.jpg"
        page.update()

    def img_merge(e):
        pass

    page.title = "ImT"
    page.add(
        ft.Row(
            [
                ft.IconButton(
                    # 一个功能图标，图像压缩
                    icon=ft.icons.IMAGE,
                    icon_size=20,
                    tooltip="图像压缩",
                    on_click=img_compress
                ),
                ft.IconButton(
                    # 一个功能图标，美颜
                    icon=ft.icons.IMAGE,
                    icon_size=20,
                    tooltip="美颜",
                    on_click=img_beauty
                ),
                ft.IconButton(
                    # 一个功能图标，图像拼接
                    icon=ft.icons.IMAGE,
                    icon_size=20,
                    tooltip="图像拼接"
                )
            ]
        )
    )
    page.overlay.append(pick_files_dialog)
    # page.add(img)
    page.add(img_origin)
    page.add(img_result)
    page.update()

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "选择文件",
                    icon=ft.icons.UPLOAD_FILE,  # 这是一个上传文件的图标
                    on_click=lambda _: pick_files_dialog.pick_files(
                        # allow_multiple=True,
                        allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp"]
                    ),
                ),
                selected_files,  # 用于显示选择的文件
            ]
        )
    )


ft.app(target=main)
