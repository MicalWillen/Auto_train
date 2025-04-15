import os
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor

def process_image(file_path, output_folder, top_left, bottom_right):
    try:
        # 打开图片
        image = Image.open(file_path)
        draw = ImageDraw.Draw(image)

        # 绘制黑色矩形
        draw.rectangle([top_left, bottom_right], fill="black")

        # 保存处理后的图片
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_folder, filename)
        image.save(output_path, 'BMP')
        print(f"Processed and saved: {output_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def mask_rectangle_multithread(folder_path, output_folder, top_left, bottom_right, max_workers=4):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取文件夹中的所有BMP文件
    bmp_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.bmp')]

    # 使用线程池进行并行处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务到线程池
        futures = [executor.submit(process_image, bmp_file, output_folder, top_left, bottom_right) for bmp_file in bmp_files]

        # 等待所有任务完成
        for future in futures:
            future.result()  # 等待每个任务完成

# 使用例子
input_folder = r"D:\xinwu_yolo\yolov50628\yolo0910-org\785-ALL\youmoqu\15-2_3\ori"  # 替换为实际输入文件夹路径
output_folder = r"D:\xinwu_yolo\yolov50628\yolo0910-org\785-ALL\youmoqu\15-2_3\c3" # 替换为实际输出文件夹路径
# top_left = (1305, 672)
# bottom_right = (5192, 6240)

# top_left = (898, 672)
# bottom_right = (4789, 5432)

top_left = (902, 0)
bottom_right = (4782, 4755)
max_threads = 8  # 可根据 CPU 核心数量调整线程数

mask_rectangle_multithread(input_folder, output_folder, top_left, bottom_right, max_workers=max_threads)

#
# # 使用例子
# input_folder = r"\\10.10.8.209\Data\YOLO资料整理\data\yolo0910\1709"  # 替换为实际输入文件夹路径
# output_folder = r"\\10.10.8.209\Data\YOLO资料整理\data\yolo0910\1709_black_mask" # 替换为实际输出文件夹路径
# top_left = (2384, 637)
# bottom_right = (7596 - 2290+15, 7496 - 650+15)
#
# mask_rectangle(input_folder, output_folder, top_left, bottom_right)
