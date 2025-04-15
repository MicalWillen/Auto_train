import os
import shutil
import json
from tqdm import tqdm

# 定义 A, B, C 文件夹路径
# src_folder_A = r"G:\app_com\mmdetection\data\Console_sliced\train_and_val"
src_folder_A = r"/data0/Colin/yolov5/datasets/CELL/0111/CELL/m01d06_station6_meta_v60_A_v1_dakuangbiaozhu_daqipao/temp"
refer_folder_B = r"/data0/Colin/yolov5/datasets/CELL/0111/CELL/m01d06_station6_meta_v60_A_v1_dakuangbiaozhu_daqipao/images/val"
target_folder_C = r"/data0/Colin/yolov5/datasets/CELL/0111/CELL/m01d06_station6_meta_v60_A_v1_dakuangbiaozhu_daqipao/labels/val"
# shutil.rmtree(target_folder_C)
os.makedirs(target_folder_C,exist_ok=True)

filenames = os.listdir(refer_folder_B)

# 遍历 A 文件夹下的文件
index = 0
for file_name in tqdm(filenames):
    try:
        # file_name = file_name[:-4]+".json"
        # file_name = file_name[:-4] +"   "+ ".jpg"
        # if not os.path.exists(os.path.join(src_folder_A, file_name)):
        #     continue
        # file_path_A = os.path.join(src_folder_A, file_name)
        # file_path_C = os.path.join(target_folder_C, file_name)
        # shutil.copyfile(file_path_A, file_path_C)
        # print(f"{file_path_A} TO {file_path_C}")

        file_name = file_name[:-4] + ".txt"
        # file_name = file_name[:-4] + ".txt"
        # file_name = file_name[:-5]+ ".jpg"
        # if not os.path.exists(os.path.join(src_folder_A, file_name)):
        #     continue
        file_path_A = os.path.join(src_folder_A, file_name)
        file_path_C = os.path.join(target_folder_C, file_name)
        # shutil.copy(file_path_A, file_path_C)
        shutil.move(file_path_A, file_path_C)
        print(f"{file_path_A} TO {file_path_C}")
        index+=1

    except Exception as e:
        # print(e)
        a=1
print(f"Index:{index}")

# refer_filenames = os.listdir(refer_folder_B)
# filenames = os.listdir(src_folder_A)
# # # 遍历 A 文件夹下的文件
# for file_name in tqdm(filenames):
#     if file_name not in refer_filenames:
#         file_path_A = os.path.join(src_folder_A, file_name)
#         file_path_C = os.path.join(target_folder_C, file_name)
#         print(f"{file_path_A} TO {file_path_C}")
#         shutil.copyfile(file_path_A, file_path_C)



