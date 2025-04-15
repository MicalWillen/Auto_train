import os

def map_category(old_category, mapping_dict):
    return mapping_dict.get(old_category, old_category)

def update_yolo_annotations(input_file, mapping_dict):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split(' ')
        if len(parts) == 5:
            old_category = int(parts[0])
            new_category = map_category(old_category, mapping_dict)
            updated_line = f"{new_category} {' '.join(parts[1:])}\n"
            updated_lines.append(updated_line)

    with open(input_file, 'w') as file:
        file.writelines(updated_lines)


path = r'/data0/Colin/yolov5/datasets/CELL/0111/CELL/m05d09_station7_light_v1/labels/val'

files = []
mapping_dict = {8: 5}
for file in os.listdir(path):
    if file.endswith(".txt"):
        file=path+'/'+file
        update_yolo_annotations(file, mapping_dict)


