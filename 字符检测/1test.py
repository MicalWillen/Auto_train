import cv2
import numpy as np
import pytesseract

# 读取图片
image = cv2.imread(r'D:\Document\desktop\1-1.bmp', cv2.IMREAD_GRAYSCALE)

# 定义一个核
kernel = np.ones((2,2), np.uint8)
_, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
# 对图片进行腐蚀操作
eroded_image = cv2.erode(image, kernel, iterations=3)
dilated_image = cv2.dilate(eroded_image, kernel, iterations=8)
eroded_image = cv2.erode(dilated_image, kernel, iterations=4)
dilated_image = cv2.dilate(eroded_image, kernel, iterations=4)
# eroded_image = cv2.erode(dilated_image, kernel, iterations=4)
# 显示腐蚀后的图片
cv2.imshow('Eroded Image', dilated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存腐蚀后的图片
cv2.imwrite('eroded_image.jpg', eroded_image)

# # 设置Tesseract-OCR的路径
# pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'  # 你需要将路径替换为你的Tesseract安装路径

# # 读取图片
# image = cv2.imread(r'D:\Document\desktop\1-1.bmp')

# # 转换图片为灰度图（可选，但有助于提高识别精度）
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 使用pytesseract进行OCR，指定中文语言
# text = pytesseract.image_to_string(gray_image, lang='chi_sim')

# # 打印识别的文本
# print(text)
