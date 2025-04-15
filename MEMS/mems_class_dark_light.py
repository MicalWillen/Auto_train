import os
import re
import shutil
from tqdm import tqdm


def mk_picture_class(file_path):
    # 定义目标文件夹
    dark_folder = "m1_dark"
    light_folder = "m1_light"
    
    # 确保目标文件夹存在
    os.makedirs(os.path.join(file_path, dark_folder), exist_ok=True)
    os.makedirs(os.path.join(file_path, light_folder), exist_ok=True)
    
    for filename in tqdm(os.listdir(file_path)):
        # 忽略目录和非文件
        if not os.path.isfile(os.path.join(file_path, filename)):
            continue
        
        # 提取文件名中的最后一个数字
        matches = re.findall(r'\d+', filename)
        if matches:
            last_digit = matches[-1]
            if last_digit == '1':
                dest_folder = dark_folder
            elif last_digit == '0':
                dest_folder = light_folder
            else:
                continue  # 如果最后一个数字不是0或1，跳过该文件

            # 移动文件
            src_file = os.path.join(file_path, filename)
            dest_file = os.path.join(file_path, dest_folder, filename)
            shutil.move(src_file, dest_file)
        else:
            print(f"No digits found in filename: {filename}")

file_path = r'D:\MeMs\每日存\1023\labeled'
mk_picture_class(file_path)