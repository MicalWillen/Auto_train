from PIL import Image, ImageEnhance

from PIL import Image

def apply_to_image(img,strength):
        """
        将亮度调整应用于图像。
        :param img: 输入的 PIL 图像
        :return: 调整后的图像
        """
        # 获取灰度强度
        # qcolor = img.color()
        # if not qcolor:
        #     return img  # 如果返回 None，直接返回原图像



        # 调整图像亮度
        pixels = img.load()  # 获取图像像素
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]  # 获取原始 RGB 值
                # 调整 RGB 值，按比例增加或减少亮度
                r = min(max(int(r * strength / 255), 0), 255)
                g = min(max(int(g * strength / 255), 0), 255)
                b = min(max(int(b * strength / 255), 0), 255)
                pixels[x, y] = (r, g, b)

        return img


# def increase_brightness_manual(image_path, increment=10):
#     img_enhanced.putdata(new_pixels)
#     # 增加亮度
#     new_pixels = []
#     for pixel in pixels:
#         r, g, b = pixel
#         r = min(r - increment, 255)  # 确保不超过最大值 255
#         g = min(g - increment, 255)
#         b = min(b - increment, 255)
#         new_pixels.append((r, g, b))
    
#     return new_pixels
image_path=r"D:\VGA\apple\result6\图片1_图片1_图片1.png"
strength=230
# 打开图片
img = Image.open(image_path)
image=apply_to_image(img,strength)

# pixels = list(img.getdata())  # 获取图像的像素数据

# 创建新的图片
# img_enhanced = Image.new(img.mode, img.size)


# increase_brightness_manual(r"D:\VGA\apple\result6\图片1_图片1_图片1.png", increment=50)
# 显示或保存增强后的图片
image.show()
image.save("brightened_image_manual.jpg")

# # 示例使用
# img = Image.open(r"D:\VGA\apple\result6\图片1_图片1_图片1.png")  # 替换为你的图片路径
# brightness_percentage = 90 # 设置亮度百分比（例如，80）

# # 调整亮度
# adjusted_img = adjust_image_brightness(img, brightness_percentage)
# adjusted_img = adjust_image_brightness(adjusted_img, brightness_percentage)
# adjusted_img = adjust_image_brightness(adjusted_img, brightness_percentage)
# adjusted_img = adjust_image_brightness(adjusted_img, brightness_percentage)
# adjusted_img = adjust_image_brightness(adjusted_img, brightness_percentage)

# # 显示或保存调整后的图像
# adjusted_img.show()
# adjusted_img.save("adjusted_image.jpg")
