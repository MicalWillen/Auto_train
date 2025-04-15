import os

from tqdm import tqdm

def convert_to_xywh(x1, y1, x2, y2):
    # 计算中心点 (x, y)
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    
    # 计算宽度和高度 (w, h)
    w = x2 - x1
    h = y2 - y1
    
    return x, y, w, h

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 5:  # 检查是否有五个部分 
            label, x1, y1, x2, y2 = map(float, parts)
            x, y, w, h = convert_to_xywh(x1, y1, x2, y2)
            label=int(label)
            new_line = f"{label} {x} {y} {w} {h}\n"
            new_lines.append(new_line)

    # 将结果写回文件
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

def process_folder(folder_path):
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            process_file(file_path)

# 使用示例
folder_path = r"D:\Document\文档\WXWork\1688855780506589\Cache\File\2024-09\12"  # 修改为你的文件夹路径
process_folder(folder_path)
