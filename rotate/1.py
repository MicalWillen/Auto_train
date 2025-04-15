import numpy as np

files = ['60_5_rotate-1.bmp', '60_5_rotate-2.bmp', '60_5_rotate1.bmp', '60_5_rotate2.bmp']
selected_table = []
kill_table = []

# 创建files的副本，避免在迭代时修改列表
files_copy = files[:]

for file in files_copy:
    if "_rotate-2" not in file and "_rotate-1" not in file and "_rotate1" not in file and "_rotate2" not in file:
        # 将文件添加到 selected_table（作为列表）
        selected_table.append([file])
        # 从原列表中移除该文件
        files.remove(file)

# 将修改后的 files 列表存入 kill_table
kill_table.append(files)

print("Selected Table:", selected_table)
print("Kill Table:", kill_table)
