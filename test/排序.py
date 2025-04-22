import os

def rename_files_in_folders(base_path):
    for root, dirs, files in os.walk(base_path):
        files.sort()  # 确保文件按顺序重命名
        for index, file in enumerate(files):
            file_extension = os.path.splitext(file)[1]  # 获取文件扩展名
            new_name = f"{index:03d}{file_extension}"  # 按规则生成新文件名
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")

# 指定需要操作的文件夹路径
folder_path = "/home/ps/Desktop/test_img（复件）"
rename_files_in_folders(folder_path)