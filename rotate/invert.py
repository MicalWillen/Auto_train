from PIL import Image
import os

# 设置输入和输出文件夹路径
input_folder = r'D:\VGA\apple\result6'
output_folder = r'D:\VGA\apple\test1'

# 如果输出文件夹不存在，创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历文件夹中的所有图片文件
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # 打开图片
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # 转化为反色
        inverted_img = Image.eval(img, lambda x: 255 - x)

        # 保存反色图片
        output_path = os.path.join(output_folder, filename)
        inverted_img.save(output_path)

        print(f"已保存反色图片：{output_path}")
