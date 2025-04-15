# import os
# import shutil
# from tqdm import tqdm


# folder = r'D:\国显\原图图片'
# output_folder = r"D:\国显\1"
# # images = ["F_64gray", "F_128gray", "F_black", "F_blue", "F_EVEN", "F_green", "F_red", "F_white"]

# # 遍历所有子文件夹
# for folder_name in tqdm(os.listdir(folder), desc="Processing Folders"):
#     current_folder = os.path.join(folder, folder_name)
#     outimage_folder = os.path.join(output_folder, folder_name)
#     for i in os.listdir(current_folder):
#         if i=="classes.txt":
#             continue
#         src_path=os.path.join(current_folder,i)
#         name=folder_name+'_'+i
#         dest_path=os.path.join(output_folder,name)
#         # 移动文件
#         shutil.copy2(src_path, dest_path)    
import os
import shutil
#修改名字为文件夹名+文件名，避免每个文件夹中文件名一样无法训练
# 定义源文件夹和目标文件夹路径
source_folder = r"D:\国显\4\2"  # 替换为包含文件的文件夹路径
destination_folder = r"D:\国显\4\2_black"  # 替换为目标文件夹路径

# 确保目标文件夹存在
os.makedirs(destination_folder, exist_ok=True)

# 遍历源文件夹中的文件
for filename in os.listdir(source_folder):
    if "black" in filename:  # 如果文件名中包含 "black"
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)
        shutil.move(source_path, destination_path)  # 移动文件
        print(f"Moved: {filename} -> {destination_folder}")

print("文件移动完成！")
