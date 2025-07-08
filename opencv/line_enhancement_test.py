
import cv2
import numpy as np
import os

# 设置图像路径
input_path = '/home2/微信图片_2025-07-04_094002_030.png'  # 替换为你的图片路径
output_dir = '/home/ps/AB/Code/1/opencv/test'

os.makedirs(output_dir, exist_ok=True)

# Step 1: 加载图像并灰度化
img = cv2.imread(input_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Step 2: 锐化增强（Unsharp Masking）
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
sharp = cv2.addWeighted(gray, 3, blurred, -2, -100)

# Step 3: 自适应 Canny 边缘检测
v = np.median(sharp)
lower = int(max(0, 0.66 * v))
upper = int(min(255, 1.33 * v))
edges = cv2.Canny(sharp, lower, upper)

# Step 4: 形态学操作 - 膨胀连接线条
kernel = np.ones((3, 3), np.uint8)
edges_dilated = cv2.dilate(edges, kernel, iterations=1)
edges_closed = cv2.morphologyEx(edges_dilated, cv2.MORPH_CLOSE, kernel)

# Step 5: 保存图像
cv2.imwrite(os.path.join(output_dir, 'gray.jpg'), gray)
cv2.imwrite(os.path.join(output_dir, 'sharp.jpg'), sharp)
cv2.imwrite(os.path.join(output_dir, 'edges.jpg'), edges)
cv2.imwrite(os.path.join(output_dir, 'enhanced_edges.jpg'), edges_closed)

print("图像处理完成，已保存至", output_dir)
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # 读取图像
# image = cv2.imread("/home2/微信图片_2025-07-04_094002_030.png")  # 替换为你的图像路径
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 1. 锐化增强
# blurred = cv2.GaussianBlur(gray, (3, 3), 0)
# sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)

# # 2. 边缘检测
# edges = cv2.Canny(sharpened, 50, 150)

# # 3. 形态学增强
# kernel = np.ones((3, 3), np.uint8)
# dilated = cv2.dilate(edges, kernel, iterations=1)
# closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

# # 4. 查找轮廓
# contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # 5. 构建 mask（选面积最大的轮廓）
# mask = np.zeros_like(gray)
# min_area = 500  # 可调参数
# for cnt in contours:
#     if cv2.contourArea(cnt) > min_area:
#         cv2.drawContours(mask, [cnt], -1, 255, thickness=cv2.FILLED)

# # 6. 显示和保存
# cv2.imwrite("top_surface_mask.png", mask)
# print("已生成 mask：top_surface_mask.png")
