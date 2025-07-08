import os

def map_category(old_category, mapping_dict):
    """根据映射字典更换类别"""
    return mapping_dict.get(old_category, old_category)

def update_yolo_segmentation_annotations(input_file, mapping_dict):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[0].isdigit():
                old_category = int(parts[0])
                new_category = map_category(old_category, mapping_dict)
                updated_line = f"{new_category} {' '.join(parts[1:])}\n"
                updated_lines.append(updated_line)
            else:
                print(f"[跳过] 格式错误的行: {input_file} -> {line.strip()}")

        with open(input_file, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)

        print(f"[完成] 已更新: {input_file}")
    except Exception as e:
        print(f"[错误] 处理文件失败 {input_file}: {e}")

# 设置路径和映射字典
path = r'/home2/item/jinlong/DCFZ-cut/git/jiaqi/re/yolov5_img_train/labels/test'
# mapping_dict = { 1: 2, 2: 3}
mapping_dict = {3:0,1:0}
# 遍历路径下的所有 .txt 文件并更新
for filename in os.listdir(path):
    if filename.endswith(".txt"):
        file_path = os.path.join(path, filename)
        update_yolo_segmentation_annotations(file_path, mapping_dict)