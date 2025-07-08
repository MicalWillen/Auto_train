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


path = r'/home/ps/AB/framework/rf-detr-develop/pridect/24/picture/type_3'

category_to_remove = 2
for file in os.listdir(path):
    if file.endswith(".txt"):
        file_path = os.path.join(path, file)
        update_yolo_annotations(file_path, category_to_remove)

