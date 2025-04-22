import os
import shutil
from concurrent.futures import ThreadPoolExecutor

def copy_images(src_folder, target_folder):
    # 创建目标文件夹
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 定义一个函数来处理每个子文件夹
    def process_sub_folder(sub_folder_path, target_sub_folder):
        if not os.path.exists(target_sub_folder):
            os.makedirs(target_sub_folder)
        
        for entry in os.scandir(sub_folder_path):
            if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                src_file_path = entry.path
                target_file_path = os.path.join(target_sub_folder, entry.name)
                
                base_name, extension = os.path.splitext(entry.name)
                counter = 1
                while os.path.exists(target_file_path):
                    target_file_path = os.path.join(target_sub_folder, f"{base_name}_{counter}{extension}")
                    counter += 1
                
                shutil.copy2(src_file_path, target_file_path)
                print(f"复制文件：{src_file_path} -> {target_file_path}")

    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=8) as executor:
        for root, dirs, _ in os.walk(src_folder):
            for dir_name in dirs:
                if dir_name in ["定位相机拍照", "OP面拍照1", "OP面拍照2","曲轴缸壁1", "曲轴缸壁2", "曲轴缸壁3", "曲轴缸壁4", "OP面拍照","OP面拍照1","TC面拍照","打刻面拍照"]:
                    sub_folder_path = os.path.join(root, dir_name)
                    target_sub_folder = os.path.join(target_folder, dir_name)
                    executor.submit(process_sub_folder, sub_folder_path, target_sub_folder)

# 指定源文件夹和目标文件夹
source_folder = "20250414-3/结果图"  # 源文件夹路径
destination_folder = "20250211-1-pre"  # 目标文件夹路径，和img同级

# 执行复制操作
copy_images(source_folder, destination_folder)
