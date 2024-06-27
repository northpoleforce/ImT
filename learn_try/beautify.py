import cv2
import numpy as np


# 美颜滤镜
def apply_beauty_filter(img):
    # # 读取图像
    # img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用 OpenCV 的人脸检测器加载预训练模型
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # 对每个检测到的人脸应用美颜滤镜
    for (x, y, w, h) in faces:
        face_roi = img[y:y+h, x:x+w]
        # 转换为浮点数以进行更精细的处理
        face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        # 高斯模糊，减少噪声和细节
        gaussian_blur = cv2.GaussianBlur(face_roi, (15, 15), 0)
        # 创建高频图像
        high_pass = face_roi - gaussian_blur
        # 增强细节
        face_roi = face_roi + high_pass * 0.5
        face_roi = np.clip(face_roi, 0, 1)
        # 转换回 8 位图像
        face_roi = (face_roi * 255).astype(np.uint8)
        face_roi = cv2.cvtColor(face_roi, cv2.COLOR_RGB2BGR)
        # 应用双边滤波以平滑皮肤
        face_roi = cv2.bilateralFilter(face_roi, 15, 75, 75)
        # 将美颜处理后的区域放回原图
        img[y:y+h, x:x+w] = face_roi
    # return img
    cv2.imwrite('beautified_image.jpg', img)
    print("美颜后的图像已保存为 beautified_image.jpg")


# 测试美颜功能
# beautified_img = (
# apply_beauty_filter(cv2.imread('image2.jpeg'))     # 原图像路径