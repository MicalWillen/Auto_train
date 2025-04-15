import numpy as np
import cv2
import matplotlib.pyplot as plt

def nearest_neighbor_interpolation(src, dst_shape):
    H_src, W_src = src.shape[:2]
    H_dst, W_dst = dst_shape

    # 创建目标图像
    dst = np.zeros((H_dst, W_dst, src.shape[2]), dtype=src.dtype)

    for y_dst in range(H_dst):
        for x_dst in range(W_dst):
            # 计算源图像中的坐标
            x_src = int(x_dst * W_src / W_dst)
            y_src = int(y_dst * H_src / H_dst)
            # 赋值给目标图像
            dst[y_dst, x_dst] = src[y_src, x_src]

    return dst

# 读取原始图像
src_image = cv2.imread(r'D:\Document\desktop\1\1-3.bmp')
# 指定目标图像的尺寸
dst_shape = (300, 400)  # 高度 x 宽度
# 进行最近邻插值
dst_image = nearest_neighbor_interpolation(src_image, dst_shape)

# 显示结果
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Resized Image (Nearest Neighbor)')
plt.imshow(cv2.cvtColor(dst_image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()
