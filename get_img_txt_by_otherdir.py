import os
import shutil

# 原图所在文件夹
source_img_dir = '/home2/item/RFDETR/进模型/0627-1'
# 查找图片和txt的目标文件夹
target_dir = '/home2/item/RFDETR/每日存/166-1_cropped'
# 输出保存目录
output_dir = '/home2/item/RFDETR/进模型/0627-1-1'

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 支持的图片扩展名
img_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.tif']

# 遍历原图文件夹中的所有图片
for fname in os.listdir(source_img_dir):
    name, ext = os.path.splitext(fname)
    if ext.lower() in img_exts:
        target_img_path = os.path.join(target_dir, fname)
        target_txt_path = os.path.join(target_dir, name + '.txt')

        # 拷贝同名图片
        if os.path.exists(target_img_path):
            shutil.copy(target_img_path, os.path.join(output_dir, fname))
            print(f"Copied image: {fname}")
        else:
            print(f"Image not found: {fname}")

        # 拷贝对应txt
        if os.path.exists(target_txt_path):
            shutil.copy(target_txt_path, os.path.join(output_dir, name + '.txt'))
            print(f"Copied label: {name}.txt")
        else:
            print(f"Label not found: {name}.txt")
