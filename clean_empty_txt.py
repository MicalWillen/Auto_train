import os
from tqdm import tqdm

# 删除空的 .txt 文件
root = r"D:\国显\4\cut\2_black_cut"

# 确保路径存在
if not os.path.exists(root):
    print(f"路径不存在: {root}")
else:
    # 保存所有 .txt 文件名（不带扩展名）
    txt_namelist = []

    for filename in tqdm(os.listdir(root), desc="扫描文件"):
        if filename.endswith(".txt"):
            file_path = os.path.join(root, filename)
            # 检查是否为空文件
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)  # 删除空文件
                print(f"已删除空文件: {file_path}")
            else:
                txt_namelist.append(filename[:-4])

    # 打印结果
    print(f"扫描完成，共找到 {len(txt_namelist)} 个非空的 .txt 文件。")
    print("文件名列表:", txt_namelist)
