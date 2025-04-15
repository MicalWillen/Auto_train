import os
from tqdm import tqdm
import shutil
# 将文件夹路径放到这里
root = r"D:\Document\文档\WXWork\1688855780506589\Cache\File\2025-03\NG\2L0YNC6H2706J4_1\labeled"
labeled_folder = os.path.join(root, "labeled")
if not os.path.exists(labeled_folder):
    os.makedirs(labeled_folder)
file_groups = {}
# 遍历所有文件名，将同名文件放入labeled_folder
for root_dir, _, files in os.walk(root):
    for file in files:
        file_name, file_ext = os.path.splitext(file)
        if file_name not in file_groups:
            file_groups[file_name] = []
        file_groups[file_name].append(os.path.join(root_dir, file))

# 将同名文件移动到labeled_folder
for file_name, file_paths in file_groups.items():
    if len(file_paths) == 2:
        for file_path in file_paths:
            shutil.move(file_path, os.path.join(labeled_folder, os.path.basename(file_path)))

