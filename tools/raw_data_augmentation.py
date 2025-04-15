import os
import shutil
import json
from tqdm import tqdm
import pickle




def creat(save_path,target_folder_C):
    os.makedirs(target_folder_C,exist_ok=True)


    with open(save_path, 'rb') as f:
        filenames = pickle.load(f)
    # 遍历 A 文件夹下的文件
    index = 0
    for file_name in tqdm(filenames):
        try:

            file_path_A = os.path.join(src_folder_A, file_name)
            file_path_C = os.path.join(target_folder_C, file_name)
            shutil.copy2(file_path_A, file_path_C)
            print(f"{file_path_A} TO {file_path_C}")
            index+=1

        except Exception as e:
            print(e)
            a=1
    print(f"Index:{index}")


def move_files_to_outer_folder(folder_path):
    # 获取文件夹下的所有文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        # 跳过根目录
        if root == folder_path:
            continue
        
        for file in files:
            # 构建文件的原始路径和目标路径
            src_path = os.path.join(root, file)
            dest_path = os.path.join(folder_path, file)
            
            # 检查目标路径是否已存在相同文件，如果存在，添加后缀避免覆盖
            if os.path.exists(dest_path):
                base, extension = os.path.splitext(file)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(folder_path, f"{base}_{counter}{extension}")
                    counter += 1
            
            # 移动文件
            shutil.move(src_path, dest_path)
    
    # 删除空的子文件夹
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # 如果目录为空
                os.rmdir(dir_path)

# 示例用法
# move_files_to_outer_folder('/path/to/your/folder')


if __name__ == '__main__':    
    # #23行设置copy2或者mv
    # #先进行数据增强，增强结束后将最外层路径给Yolo变量
    # # 只留最外层
    # Yolo=r"/data0/Colin/yolov5/datasets/CELL/0111/CELL/temp/3_dark"
    # move_files_to_outer_folder(Yolo)

    # #清洗完之后的数据
    src_folder_A = r"/data0/Colin/yolov5/datasets/CELL/0111/temp/3_dark_1"

    #原始数据
    root = r"/data0/Colin/yolov5/datasets/CELL/0111/CELL/m01d06_station3_v67_cleanedDefect3_JiZhuFuShi"
    #保存pkl路径
    save_root = r"/data0/Colin/yolov5/datasets/CELL/0111/PKL"
    #最后数据集存放目录
    target_folder_C = r"/data0/Colin/yolov5/datasets/CELL/0111/temp/m01d06_station3_v67_cleanedDefect3_JiZhuFuShi"
    # pickle_refer_folder_B = r"/mnt/nvme0n1/Colin/yolov5s/datasets/CELL/0423beifen/m01d06_station6_meta_v60_A_v1_dakuangbiaozhu_daqipao_NameList/img_train.pkl"





    img_train = os.listdir(os.path.join(root,"images/train"))
    img_val = os.listdir(os.path.join(root,"images/val"))
    label_train = os.listdir(os.path.join(root,"labels/train"))
    label_val = os.listdir(os.path.join(root,"labels/val"))

    save_img_train = os.path.join(target_folder_C,"images/train")
    save_img_val = os.path.join(target_folder_C,"images/val")
    save_label_train = os.path.join(target_folder_C,"labels/train")
    save_label_val = os.path.join(target_folder_C,"labels/val")



    os.makedirs(save_root,exist_ok=True)

    save_path = os.path.join(save_root,"img_train.pkl")
    with open(save_path, 'wb') as f:
        pickle.dump(img_train, f)
    creat(save_path,save_img_train)

    save_path = os.path.join(save_root,"img_val.pkl")
    with open(save_path, 'wb') as f:
        pickle.dump(img_val, f)
    creat(save_path,save_img_val)

    save_path = os.path.join(save_root,"label_train.pkl")
    with open(save_path, 'wb') as f:
        pickle.dump(label_train, f)
    creat(save_path,save_label_train)

    save_path = os.path.join(save_root,"label_val.pkl")
    with open(save_path, 'wb') as f:
        pickle.dump(label_val, f)
    creat(save_path,save_label_val)





