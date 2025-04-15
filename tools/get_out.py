import os
import shutil
import json
from tqdm import tqdm
import pickle
def move_files_to_outer_folder(folder_path):
    # 获取文件夹下的所有文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 构建文件的原始路径和目标路径
            src_path = os.path.join(root, file)
            dest_path = os.path.join(folder_path, file)
            # 移动文件
            shutil.move(src_path, dest_path)
Yolo=r"/data1/lhl/MEMS/station1_light"
move_files_to_outer_folder(Yolo)