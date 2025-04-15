import os
from tqdm import tqdm
import shutil

# 将文件夹路径放到这里
root = r"D:\MeMs\test"
labeled_folder = os.path.join(root, "labeled")

# Create the labeled folder if it does not exist
if not os.path.exists(labeled_folder):
    os.makedirs(labeled_folder)

# Collect and group files by the prefix before the first underscore
file_groups = {}

for filename in tqdm(os.listdir(root)):
    if filename.endswith((".bmp", ".txt")):
        # prefix = filename.split('_')[0]
        prefix = filename.rsplit('-', 1)[0]
        if prefix not in file_groups:
            file_groups[prefix] = []
        file_groups[prefix].append(filename)

# Process each group
for prefix, files in file_groups.items():
    if len(files) >=3:
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(labeled_folder, file)
            shutil.copy(source_path, destination_path)

print("Processing completed.")
