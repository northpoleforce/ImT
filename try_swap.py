import flet
from flet import (
    Column,
    Container,
    Draggable,
    DragTarget,
    DragTargetAcceptEvent,
    Page,
    Row,
    border,
    colors,
)

def main(page: Page):
    page.title = "拖动图片示例"

    # 创建两个Draggable对象，每个对象都有一个图片
    draggable1 = Draggable(
        group="photo",
        content=flet.Image(
            src="image1.jpg",
            width=200,
            height=200,
            fit=flet.ImageFit.NONE,
            repeat=flet.ImageRepeat.NO_REPEAT,
            border_radius=flet.border_radius.all(10),
        )
    )

    draggable2 = Draggable(
        group="photo",
        content=flet.Image(
            src="beautified_image.jpg",
            width=200,
            height=200,
            fit=flet.ImageFit.NONE,
            repeat=flet.ImageRepeat.NO_REPEAT,
            border_radius=flet.border_radius.all(10),
        )
    )

    # 创建两个DragTarget对象，每个对象都与一个Draggable对象关联
    def drag_accept(e: DragTargetAcceptEvent):
        # 当一个Draggable对象被拖动到一个DragTarget对象上时，交换两个Draggable对象的图片
        src = page.get_control(e.src_id)
        temp = src.content.src
        src.content.src = e.control.content.src
        e.control.content.src = temp
        src.update()
        e.control.update()

    drag_target1 = DragTarget(
        group="photo",
        content=draggable1.content,
        on_accept=drag_accept,
    )

    drag_target2 = DragTarget(
        group="photo",
        content=draggable2.content,
        on_accept=drag_accept,
    )

    # 将Draggable对象和DragTarget对象添加到页面上
    page.add(
        Row(
            [
                Column([draggable1, drag_target1]),
                Column([draggable2, drag_target2]),
            ]
        )
    )

flet.app(target=main)