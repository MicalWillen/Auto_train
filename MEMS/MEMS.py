import os
#将标注中的两个空格改为一个
# 定义文件夹路径
folder_path = 'D:\Document\desktop\SelectYOLO'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否为txt文件
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        
        # 替换两个空格为一个空格
        modified_data = data.replace('  ', ' ')
        
        # 将修改后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_data)

print("所有文件已处理完毕")