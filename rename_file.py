# import os
# import re

# # 设置目标路径
# folder_path = "/home2/item/jinlong/DCFZ/进模型/111"  # 请替换为你的实际路径

# # 遍历文件夹中的文件
# for filename in os.listdir(folder_path):
#     if filename.endswith(".txt") or filename.endswith(".jpg"):
#         # 匹配以 1_ 或 2_ 开头，后面带时间戳的部分
#         match = re.search(r'(\d+(?:_\d+)+)(\.\w+)$', filename)
#         if match:
#             new_name = match.group(1) + match.group(2)
#             old_path = os.path.join(folder_path, filename)
#             new_path = os.path.join(folder_path, new_name)
#             if old_path != new_path:
#                 os.rename(old_path, new_path)
#                 print(f"重命名: {filename} → {new_name}")
import os

folder = "/home2/datsests/MOT/MOT20/train/train/img5"  # 替换为实际路径

# 找出所有 .jpg 和 .png 文件（假设每张图片都有对应的 .txt）
image_files = sorted([f for f in os.listdir(folder) if f.endswith((".jpg", ".png"))])
counter = 2835

for image in image_files:
    base_name = os.path.splitext(image)[0]
    txt = base_name + ".txt"
    image_path = os.path.join(folder, image)
    txt_path = os.path.join(folder, txt)

    if not os.path.exists(txt_path):
        # 如果没有对应的 txt 文件，则创建一个空的 txt 文件
        with open(txt_path, 'w') as f:
            f.write("")  # 创建空文件
        print(f"创建空的 txt 文件: {txt}")

    new_base = f"{counter:03d}"
    new_image = os.path.join(folder, new_base + os.path.splitext(image)[1])
    new_txt = os.path.join(folder, new_base + ".txt")
    
    os.rename(image_path, new_image)
    os.rename(txt_path, new_txt)
    print(f"重命名: {image} → {new_base}{os.path.splitext(image)[1]}, {txt} → {new_base}.txt")
    
    counter += 1
