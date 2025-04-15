import os
import shutil
from tqdm import tqdm
import csv

# 统计数据集的各类缺陷次数
def count_defects_in_files(root_folder):
    """
    统计并返回指定目录下每个txt文件中缺陷类型的出现次数，并检查是否存在同名图片。
    """
    defect_counts = {}

    for filename in os.listdir(root_folder):
        if filename.endswith(".txt"):
            txt_name = os.path.splitext(filename)[0]
            file_path = os.path.join(root_folder, filename)

            try:
                with open(file_path, "r") as f:
                    for line in f:
                        try:
                            defect_type = int(line.split()[0])
                            if defect_type not in defect_counts:
                                defect_counts[defect_type] = 0
                            defect_counts[defect_type] += 1
                        except ValueError:
                            continue
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return defect_counts

# 将数据集依据缺陷类型移动文件到对应缺陷目录子文件夹中
def move_files_by_defect_type(fileroot, picked_root, defect_types):
    """
    根据指定的缺陷类型范围，将源文件夹中的图片和标注文件移动到目标文件夹下的对应子文件夹中。
    如果没有找到图片，仍然会移动 .txt 文件。
    """
    os.makedirs(picked_root, exist_ok=True)

    filenames = [file for file in os.listdir(fileroot) if file.endswith(".txt")]

    for txtfile in tqdm(filenames):
        txt_path = os.path.join(fileroot, txtfile)
        base_name = txtfile[:-4]  # 去掉 .txt 扩展名

        # 尝试寻找不同扩展名的图片文件
        img_extensions = ('.jpg', '.bmp', '.png')
        img_path = None
        for ext in img_extensions:
            potential_img_path = os.path.join(fileroot, base_name + ext)
            if os.path.exists(potential_img_path):
                img_path = potential_img_path
                break

        matched_types = set()
        try:
            with open(txt_path, "r") as f:
                for line in f:
                    defect_type = int(line.split(" ")[0])
                    if defect_type in defect_types:
                        matched_types.add(defect_type)
        except Exception as e:
            print(f"Error reading {txtfile}: {e}")
            continue

        for defect_type in matched_types:
            defect_folder = os.path.join(picked_root, f"type_{defect_type}")
            os.makedirs(defect_folder, exist_ok=True)

            try:
                # 移动图片文件（如果有）
                if img_path is not None:
                    shutil.copy(img_path, os.path.join(defect_folder, os.path.basename(img_path)))

                # 总是移动 .txt 文件
                shutil.copy(txt_path, os.path.join(defect_folder, os.path.basename(txt_path)))
            except Exception as e:
                print(f"Error moving files for {txtfile} to {defect_folder}: {e}")

    print("所有文件均已处理并相应移动")

# 转换并排序缺陷类型合适的制图字典
def sort_dict_by_key_number(input_dict):
    """
    对字典按照键中的数字进行排序，并在新字典中去除'type_'前缀。
    """
    sorted_items = sorted(input_dict.items(), key=lambda item: int(item[0].split('_')[1]))
    sorted_dict = {item[0].split('_')[1]: item[1] for item in sorted_items}
    return sorted_dict

# 保存统计数据到 CSV 文件
def save_counts_to_csv(file_path, defect_counts):
    """
    将缺陷类型和对应的数量保存到 CSV 文件。
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Defect Type", "Count"])

        for defect_type, count in defect_counts.items():
            writer.writerow([defect_type, count])

    print(f"缺陷类型统计已保存到: {file_path}")

# 示例调用
root_folder = r'D:\Document\desktop\yolov5-master\yolov5-master\runs\detect\mems22'
root_directory = os.path.join(root_folder,"picture")

# 统计缺陷类型
defect_counts = count_defects_in_files(root_folder)
csv_output_path = os.path.join(root_folder, 'defect_counts.csv')

# 保存到 CSV 文件
save_counts_to_csv(csv_output_path, defect_counts)

# 移动文件到对应缺陷文件夹
move_files_by_defect_type(root_folder, root_directory, defect_counts.keys())
