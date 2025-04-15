import os
import re
import shutil
from tqdm import tqdm
def replace_L_with_L1(filename):
    # 使用正则表达式将文件名中的 L0、L1、L2 替换为 L1
    return re.sub(r'L[012]', 'L1', filename)

def process_folder(input_folder, output_folder):
    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 跳过文件名中包含 L3 的文件
        if 'L3' in filename:
            print(f"跳过文件: {filename}")
            continue

        # 构造完整的文件路径
        input_file = os.path.join(input_folder, filename)
        
        # 如果是文件而不是文件夹
        if os.path.isfile(input_file):
            # 修改文件名中的 L0, L1, L2 为 L1
            new_filename = replace_L_with_L1(filename)
            
            # 构造输出文件的路径
            output_file = os.path.join(output_folder, new_filename)
            
            # 将文件复制到新的文件夹并重命名
            shutil.copy(input_file, output_file)
            print(f"{filename} -> {new_filename}")

def mk_picture_class(file_path):
    # 定义目标文件夹
    L0_folder = "L0"
    L1_folder = "L1"
    L2_folder = "L2"
    L3_folder = "L3"
    L4_folder = "json"
    folders=[L0_folder,L1_folder,L2_folder,L3_folder,L4_folder]
    # 确保目标文件夹存在
    for folder in folders:
        os.makedirs(os.path.join(file_path, folder), exist_ok=True)
    
    for filename in tqdm(os.listdir(file_path)):
        # 忽略目录和非文件
        if not os.path.isfile(os.path.join(file_path, filename)):
            continue
        if filename.endswith(".jpg") or filename.endswith(".bmp"):
            # 提取文件名中的最后一个数字
            matches = re.findall(r'L[0123]', filename)
            if matches:
                last_digit = matches[-1]
                if last_digit == 'L0':
                    dest_folder = L0_folder
                elif last_digit == 'L1':
                    dest_folder = L1_folder
                elif last_digit == 'L2':
                    dest_folder = L2_folder
                elif last_digit == 'L3':
                    dest_folder = L3_folder
                
                else:
                    continue  # 如果最后一个数字不是0或1，跳过该文件

                # 移动文件
                src_file = os.path.join(file_path, filename)
                dest_file = os.path.join(file_path, dest_folder, filename)
                shutil.move(src_file, dest_file)
            else:
                print(f"No digits found in filename: {filename}")
        else:
            src_file = os.path.join(file_path, filename)
            dest_file = os.path.join(file_path, L4_folder, filename)
            shutil.move(src_file, dest_file)
    

file_path = r'D:\A\TC_org\正常原图\evw\EVW_DM0813'
mk_picture_class(file_path)
# 对文件夹中的文件进行批量操作



# 输入文件夹路径
# input_folder = os.path.join(file_path, "json")
# # 输出文件夹路径
# output_folder = os.path.join(file_path, "json_change")
# process_folder(input_folder, output_folder)