import os
from tqdm import tqdm
import shutil

# 将文件夹路径放到这里
root = r"D:\Document\文档\WXWork\1688855780506589\Cache\File\2025-03\NG\2L0YNC6H2706J4_1\labeled"
labeled_folder = os.path.join(root, "labeled")

# Create the labeled folder if it does not exist
if not os.path.exists(labeled_folder):
    os.makedirs(labeled_folder)

# Collect and group files by the name without extension
file_groups = {}

for filename in tqdm(os.listdir(root)):
    if filename.endswith((".jpg", ".txt")):
        name_without_ext = os.path.splitext(filename)[0]
        if name_without_ext not in file_groups:
            file_groups[name_without_ext] = []
        file_groups[name_without_ext].append(filename)

# Process each group
for name, files in file_groups.items():
    if len(files) == 2 and any(f.endswith(".bmp") for f in files) and any(f.endswith(".txt") for f in files):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(labeled_folder, file)
            shutil.copy(source_path, destination_path)

print("Processing completed.")
