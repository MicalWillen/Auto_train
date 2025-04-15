import os
import shutil
import time
import pandas as pd
from tqdm import tqdm

from clean_picture import remove_extra_files
from get_out import move_files_to_outer_folder
#需定义类别名称，再分类
# 定义classList
class_list = ["凹印", "白点", "白痕", "白线", "残胶", "CNC多铣", "CNC过铣", "多蓝膜", "多料", "打磨痕", "刀纹（刀线，震刀纹，接刀痕，盘刀纹）", "鼓包", "过磨（塌边）", "鬼影", "划伤（亮线，刮伤）", "黑线", "喇叭孔堵孔", "喇叭孔毛边", "喇叭孔异物", "漏镭雕", "亮点", "亮痕", "螺孔异物", "铝屑", "亮线", "亮印", "毛边", "麻点", "毛丝卷边（毛边）", "抛痕成像弱", "抛痕L3可见", "抛痕（打磨痕，沙痕，刷痕）", "泡棉（长、中间、短）破损", "泡棉偏位", "泡棉翘起", "泡棉（长、中间、短）缺失", "泡棉（长、中间、短）褶皱", "碰伤", "塌边", "台阶", "氧化（麻点）", "异色", "压伤（变形，凹陷,凹痕,压印，凹印，凸包，起鼓)", "异物", "针孔压伤", "脏污（水印，笔印，手指印）"]

# 创建文件夹名称到 classList 名称的映射字典
folder_to_class_map = {str(index): value for index, value in enumerate(class_list)}

def count_files_in_directory(directory_path):
    folders = {}
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.isdir(folder_path):
            file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
            file_count=file_count/2
            class_name = folder_to_class_map.get(folder_name, folder_name)  # 使用映射字典替换文件夹名称
            folders[class_name] = file_count

    sorted_folders = sorted(folders.items(), key=lambda item: item[1], reverse=True)

    # 创建 DataFrame
    df = pd.DataFrame(sorted_folders, columns=['Folder Name', 'File Count'])
    return df

def copy_files_based_on_defect_type(fileroot, picked_root, defect_types):
    os.makedirs(picked_root, exist_ok=True)
    filenames = [file for file in os.listdir(fileroot) if file.endswith(".txt")]

    for txtfile in tqdm(filenames):
        try:
            with open(os.path.join(fileroot, txtfile), "r") as f:
                anns = f.read().splitlines()
                matched_types = set()

                for ann in anns:
                    defect_type = int(ann.split(" ")[0])
                    if defect_type in defect_types:
                        matched_types.add(defect_type)

                for defect_type in matched_types:
                    defect_folder = os.path.join(picked_root, str(defect_type))
                    os.makedirs(defect_folder, exist_ok=True)

                    image_filename = txtfile[:-4] + ".jpg"
                    image_path = os.path.join(fileroot, image_filename)
                    if os.path.exists(image_path):
                        shutil.copy(image_path, os.path.join(defect_folder, image_filename))
                    else:
                        image_filename = txtfile[:-4] + ".bmp"
                        image_path = os.path.join(fileroot, image_filename)
                        if os.path.exists(image_path):
                            shutil.copy(image_path, os.path.join(defect_folder, image_filename))

                    shutil.copy(os.path.join(fileroot, txtfile), os.path.join(defect_folder, txtfile))
        except Exception as e:
            print(f"Error processing file {txtfile}: {e}")

def save_to_excel(df, output_path):
    print(f"Saving to Excel file: {output_path}")
    df.to_excel(output_path, index=False)

def main():
    fileroot = r"D:\MeMs\进模型\0727进206第a----0805进201\m1_light"
    picked_root = r"D:\MeMs\进模型\0727进206第a----0805进201\m1_light\1_37"
    defect_types = range(0, 46)  # 设置要提取的 defect_type 范围
    move_files_to_outer_folder(fileroot)
    remove_extra_files(fileroot)
    copy_files_based_on_defect_type(fileroot, picked_root, defect_types)
    df = count_files_in_directory(picked_root)
    save_to_excel(df, os.path.join(picked_root, 'file_count.xlsx'))

if __name__ == "__main__":
    main()