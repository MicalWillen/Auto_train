import os
import shutil

# 源文件夹路径（假设文件夹路径为 current_folder）
source_folder = r'D:\sabers\每日存\0306\过杀原图'  # 修改为实际的文件夹路径
# 目标文件夹路径
# target_folder = r'D:\Document\文档\WXWork\1688855780506589\Cache\File\2025-03\过杀原图/label'
target_folder = os.path.join(source_folder, "label")
# 如果目标文件夹不存在，则创建它
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 指定要筛选的 Ima 数字
selected_images = [12, 14, 18, 19, 5, 6, 7, 8]

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    # 检查文件名是否符合特定格式
    if filename.count('_') > 4:  # 确保文件名包含足够的分隔符
        # 拆分文件名
        parts = filename.split('_')

        # 检查第1部分是否是 "1" 且 "Ima" 后面的数字是否符合要求
        if parts[1] == "1" and "Ima" in parts[4]:
            try:
                # 提取 Ima 后面的数字
                image_number = int(parts[4].replace('Ima', ''))
            except ValueError:
                continue  # 如果无法转换为数字，则跳过

            # 如果图片编号在选中的列表中，则复制文件
            if image_number in selected_images:
                # 生成源文件和目标文件路径
                source_file = os.path.join(source_folder, filename)
                target_file = os.path.join(target_folder, filename)
                # 复制文件
                shutil.move(source_file, target_file)
                print(f"文件 {filename} 已复制到 {target_folder}")

print("文件筛选和复制完成。")
