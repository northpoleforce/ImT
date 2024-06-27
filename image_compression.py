import cv2


def compress_image(img, output_path, quality=90):
    # 设置压缩参数
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    # 压缩图像
    result, encimg = cv2.imencode('.jpg', img, encode_param)
    if not result:
        raise ValueError("图像压缩失败")
    # 保存压缩后的图像
    with open(output_path, 'wb') as f:
        f.write(encimg)