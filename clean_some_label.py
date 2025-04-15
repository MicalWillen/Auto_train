import os

def update_yolo_annotations(input_file, category_to_remove):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split(' ')
        if len(parts) == 5:
            category = int(parts[0])
            if category != category_to_remove:
                updated_lines.append(line)

    with open(input_file, 'w') as file:
        file.writelines(updated_lines)


path = r'D:\Document\文档\WXWork\1688855780506589\Cache\File\2025-03\NG\2L0YNC6H2706J4_1\labeled'

category_to_remove = 8
for file in os.listdir(path):
    if file.endswith(".txt"):
        file_path = os.path.join(path, file)
        update_yolo_annotations(file_path, category_to_remove)

