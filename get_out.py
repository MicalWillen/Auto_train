import os
import shutil
import json
from tqdm import tqdm
import pickle

def move_files_to_outer_folder(folder_path):
    # 获取文件夹下的所有文件夹和文件
    for root, dirs, files in os.walk(folder_path, topdown=False):  # 使用 topdown=False 以便先处理子文件夹
        for file in files:
            # 构建文件的原始路径和目标路径
            src_path = os.path.join(root, file)
            dest_path = os.path.join(folder_path, file)
            # 移动文件
            shutil.move(src_path, dest_path)
        # 删除空文件夹
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # 检查文件夹是否为空
                os.rmdir(dir_path)

Yolo = r"/home/ps/AB/item/bentian/打刻/进模型/0331/yolo"
move_files_to_outer_folder(Yolo)