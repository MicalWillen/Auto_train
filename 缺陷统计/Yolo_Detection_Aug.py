import subprocess
import pickle
import os
import random
import json
import shutil
import re
import cv2
import glob

from utils import *
from datetime import datetime
from collections import defaultdict
from PIL import Image, ImageDraw
from tqdm import tqdm

# 用于存储pkl版本号(请勿修改！)
version_file_name = 'latest_version.txt'
def create_project_structure(root_dir):
    # 定义需要创建的目录结构
    directories = [
        os.path.join(root_dir, 'temp', 'mask'),
        os.path.join(root_dir, "images", "train"),
        os.path.join(root_dir, "images", "val"),
        os.path.join(root_dir, "labels", "train"),
        os.path.join(root_dir, "labels", "val"),
        os.path.join(root_dir, 'temp', 'save'),
        os.path.join(root_dir, 'temp')
    ]

    # 创建目录
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print(f"目录结构在 '{root_dir}' 下创建完毕!")
    return directories


def move_files_to_outer_folder(folder_path):
    # 获取文件夹下的所有文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 构建文件的原始路径和目标路径
            src_path = os.path.join(root, file)
            dest_path = os.path.join(folder_path, file)
            # 移动文件
            shutil.move(src_path, dest_path)


def remove_empty_dirs(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")


def Aug(path, aug_path, Aug_methods, Aug_num):
    Aug_method_Names = ['vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise']
    # 创建数据增强子文件夹
    if not os.path.exists(os.path.join(aug_path, Aug_methods[Aug_num])):
        os.makedirs(os.path.join(aug_path, Aug_methods[Aug_num]))
    aug_path = os.path.join(aug_path, Aug_methods[Aug_num])

    cls_docs = os.listdir(path)

    cls_save_path = aug_path
    for file in tqdm(cls_docs):
        if '.ini' in file:
            break
        if '.txt' in file:
            continue
        file_name = file[0:-4]
        img_type = file[-3:]
        img_name = file_name + '.{}'.format(img_type)
        txt_name = file_name + '.txt'
        new_img = file_name + '_{}.{}'.format(Aug_method_Names[Aug_num], img_type)
        new_txt = file_name + '_{}.txt'.format(Aug_method_Names[Aug_num])
        if not os.path.exists(os.path.join(path, img_name)):
            print('image:{} not found'.format(img_name))
            continue
        # 图片操作
        img = Image.open(os.path.join(path, img_name)).convert('RGB')
        if Aug_num == 0:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            img.save(os.path.join(cls_save_path, new_img))
        elif Aug_num == 1:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img.save(os.path.join(cls_save_path, new_img))
        elif Aug_num == 2:
            img = img.rotate(180)
            img.save(os.path.join(cls_save_path, new_img))
        elif Aug_num == 3:
            img = cv2.imread(os.path.join(path, img_name))
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.imwrite(os.path.join(cls_save_path, new_img), img)
        elif Aug_num == 4:
            img = cv2.imread(os.path.join(path, img_name))
            img = cv2.flip(cv2.transpose(img), 1)
            cv2.imwrite(os.path.join(cls_save_path, new_img), img)
        else:
            print('Augmentation method not found')
        result = []
        if not os.path.exists(os.path.join(path, txt_name)):
            print(f'Text file: {txt_name} not found, creating an empty file.')
            open(os.path.join(path, txt_name), 'w').close()
        # txt操作
        with open(os.path.join(path, txt_name), encoding='utf-8') as file_obj:
            lines = file_obj.readlines()
            # 逐行读取
            for line in lines:
                number = find_number(line)
                if Aug_num == 0:
                    new_number = Vertical_flip_bbox(number)
                elif Aug_num == 1:
                    new_number = Horizontal_flip_bbox(number)
                elif Aug_num == 2:
                    new_number = rotation180_bbox(number)
                elif Aug_num == 3:
                    new_number = rotate90_bbox(number)
                elif Aug_num == 4:
                    new_number = rotate270_bbox(number)
                else:
                    print('Augmentation method not found')
                result.append(new_number)
            with open(os.path.join(cls_save_path, new_txt), 'w', encoding='utf-8') as new_file_obj:
                for k in range(len(result)):
                    for k_k in range(len(result[k])):
                        new_file_obj.write('{} '.format(result[k][k_k]))
                    new_file_obj.write('\n')


def extract_prefix(file_name):
    # 定义可能的后缀
    suffixes = ['_vertical', '_horizontal', '_rotate180', '_anticlockwise90', '_clockwise']

    # 反向查找后缀，找到最后一个匹配的后缀并获取它的位置
    for suffix in suffixes:
        if suffix in file_name:
            # 找到后缀，按_分割，取_前面的一部分
            prefix = file_name.split(suffix)[0]
            return prefix

    # 如果没有任何后缀，按.分割，取0号元素
    if '.' in file_name:
        prefix = file_name.split('.')[0]
        return prefix

    return None


def select_random_files(file_list, istrain, count=4):
    # 确保 file_list 是一个 NumPy 数组
    file_list = np.array(file_list)
    file_list_copy = file_list
    selected_table = []
    unselected_table = []
    kill_table = []

    if istrain:
        # 'vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise'
        for j, files in tqdm(enumerate(file_list)):
            for i, file in enumerate(files):
                if "vertical" not in file and "horizontal" not in file and "rotate180" not in file and "anticlockwise90" not in file and "clockwise" not in file:
                    # kill存入去除原图的文件列表
                    tmp = [files[i]]
                    selected_table.append(tmp)
                    files = np.delete(files, i)
                    kill_table.append(files)
        count -= 1
    if istrain:
        for files in kill_table:
            if len(files) < count:
                print("文件列表中文件数：" + str(len(files)))
                raise ValueError("文件列表中的文件数量少于指定的选择数量")

            # 随机选择指定数量的文件
            selected_files = random.sample(list(files), count)

            # 获取剩余未被选中的文件
            unselected_files = [file for file in files if file not in selected_files]

            # 将选中的文件和未选中的文件分别添加到各自的表中
            selected_table.append(selected_files)
            unselected_table.append(unselected_files)
    else:
        for files in file_list:
            if len(files) < count:
                raise ValueError("文件列表中的文件数量少于指定的选择数量")

            # 随机选择指定数量的文件
            selected_files = random.sample(list(files), count)

            # 获取剩余未被选中的文件
            unselected_files = [file for file in files if file not in selected_files]

            # 将选中的文件和未选中的文件分别添加到各自的表中
            selected_table.append(selected_files)
            unselected_table.append(unselected_files)

    return selected_table, unselected_table



def group_files_by_prefix(folder_path):
    # 初始化一个字典来存储文件名前缀及其对应的文件列表
    file_dict = {}

    # 遍历文件夹中的所有文件和文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 获取文件名前缀
            prefix = extract_prefix(file)
            if prefix and not file.endswith('.txt'):
                # 如果文件名前缀不在字典中，则添加进字典并初始化一个列表
                if prefix not in file_dict:
                    file_dict[prefix] = []
                # 将文件名添加到相应前缀的列表中
                file_dict[prefix].append(file)

    # 初始化一个空列表来存储具有相同前缀的文件列表
    table = []

    # 遍历字典中的值，将文件列表添加到二维表中
    for file_list in file_dict.values():
        table.append(file_list)

    return table


def blocking_mask(ori_img_dir, mask_save_dir, mask_labels):
    save_dir = mask_save_dir
    txt_dir = ori_img_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    files = os.listdir(ori_img_dir)
    for file in tqdm(files):
        if 'txt' in file:
            continue
        txt_path = os.path.join(txt_dir, file[:-4] + '.txt')
        # 通过img名字在txt路径下找txt文件
        if not os.path.exists(txt_path):
            print('{} has not label'.format(file))
            with open(txt_path, 'w') as f:
                pass

        img = cv2.imread(os.path.join(ori_img_dir, file))
        img_mask = draw_txt_mask(img, os.path.join(txt_dir, file[:-4] + '.txt'), mask_labels)

        cv2.imwrite(os.path.join(save_dir, file), img_mask)  # 保存被遮盖的图片

        filename = file[:-4]
        ori_txt = filename + '.txt'
        save_txt = filename + '.txt'

        ori_txt = os.path.join(txt_dir, ori_txt)
        save_txt = os.path.join(save_dir, save_txt)

        merger_select_label(ori_txt, save_txt, mask_labels)


def move_selected_and_unselected_files(selected_table, unselected_table, mask_save_dir, directories):
    def move_files(file_list, dest_img_dir, dest_txt_dir):
        for file in file_list:
            src_file = os.path.join(mask_save_dir, file)
            file_ext = os.path.splitext(file)[1]  # 获取文件扩展名
            if file_ext in ['.bmp', '.jpg', '.png']:  # 确保处理 .bmp 和 .jpg 文件
                dest_img_file = os.path.join(dest_img_dir, file)
                dest_txt_file = os.path.join(dest_txt_dir, file.replace(file_ext, '.txt'))
                shutil.move(src_file, dest_img_file)
                if os.path.exists(src_file.replace(file_ext, '.txt')):
                    shutil.move(src_file.replace(file_ext, '.txt'), dest_txt_file)

    # 将 selected_table 对应的文件移动到训练文件夹
    for selected_files in selected_table:
        move_files(selected_files, directories[1], directories[3])

    # 将 unselected_table 对应的文件移动到验证文件夹
    for unselected_files in unselected_table:
        move_files(unselected_files, directories[2], directories[4])


def process_and_augment_data(path, aug_path, Aug_methods, Aug_nums, mask_labels, count, istrain):
    directories = create_project_structure(aug_path)
    mask_save_dir = directories[0]
    save_dir = directories[5]
    temp = directories[6]
    blocking_mask(path, save_dir, mask_labels)
    if not os.path.exists(aug_path):
        os.makedirs(aug_path)

    for Aug_num in Aug_nums:
        Aug(save_dir, mask_save_dir, Aug_methods, Aug_num)
    move_files_to_outer_folder(mask_save_dir)
    move_files_to_outer_folder(temp)
    remove_empty_dirs(temp)
    # directories = create_project_structure(aug_path)
    group = group_files_by_prefix(temp)
    selected_table, unselected_table = select_random_files(group, istrain, count)
    move_selected_and_unselected_files(selected_table, unselected_table, temp, directories)
    shutil.rmtree(temp)

#在PKL相同根目录下创建临时目录获取新数据增强后的信息
def create_temp(orgin_path):

    dir_path = orgin_path
    # 在该目录下创建名为temp的新目录
    temp_dir_path = os.path.join(dir_path, 'temp')
    PKL_dir_path = os.path.join(dir_path, 'PKL')
    #JQ_dir_path = os.path.join(dir_path, 'JQ')
    PUBLIC_dir_path = os.path.join(dir_path, 'public')

    # 将所有需要检查的路径存储在一个列表中
    paths_to_check = [temp_dir_path,  PKL_dir_path,  PUBLIC_dir_path, ]

    # 遍历列表中的每个路径,确保路径存在
    for anypath in paths_to_check:
        if not os.path.exists(anypath):
            os.makedirs(anypath)

    return temp_dir_path, PKL_dir_path, PUBLIC_dir_path


def read_version(version_file_path):
    """
    从文件中读取当前版本号。
    如果文件不存在，则返回0.0（或您选择的初始版本号）。
    """
    try:
        with open(version_file_path, 'r') as f:
            return float(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0.0  # 或您选择的初始版本号


def write_version(version_file_path, new_version):
    """
    将新的版本号写入文件。
    """
    with open(version_file_path, 'w') as f:
        f.write(f"{new_version}\n")


def create_new_pkl(project_name, target_folder_path):
    """
    在目标文件夹中创建一个新的.pkl文件，文件名包含递增的版本号。
    """

    # 获取当前日期（月+日）
    # 获取当前日期
    now = datetime.now()

    # 格式化日期为年份后两位+月份+日
    # 注意：年份使用%y来获取后两位，月份使用%m，日使用%d
    formatted_date = now.strftime('%y%m%d')

    # 获取源文件夹名称，用作文件名前缀
    source_folder_name = os.path.basename(project_name)

    # 确定版本号文件的路径
    version_file_path = os.path.join(target_folder_path, version_file_name)

    # 读取当前版本号
    current_version = read_version(version_file_path)

    # 计算新的版本号（这里我们简单地增加0.1）
    new_version = current_version + 0.1

    # 构建新文件名
    old_file_name = f"{formatted_date }_{source_folder_name}_V{current_version:.1f}.pkl"
    new_file_name = f"{formatted_date }_{source_folder_name}_V{new_version:.1f}.pkl"
    new_file_path = os.path.join(target_folder_path, new_file_name)

        # 更新版本号文件
    write_version(version_file_path, new_version)

    print(f"新pkl文件已创建：{new_file_path}")
    return old_file_name,new_file_name

# 加强集移动到公共集
def move_files_to_source_folder(folder_path, source_folder):
    # 获取文件夹下的所有文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        # 跳过根目录
        if root == folder_path:
            continue
        for file in files:
            # # 构建文件的原始路径和目标路径
            src_path = os.path.join(root, file)
            dest_path = os.path.join(source_folder, file)
            # 存在相同的则跳过
            if os.path.exists(dest_path):
                # print(f"File {file} already exists in the destination folder. Skipping...")
                # 删除原始文件夹中的相同文件
                os.remove(src_path)
            else:
                # 移动文件
                shutil.move(src_path, dest_path)

    # 删除空的子文件夹
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # 如果目录为空
                os.rmdir(dir_path)

    print(f"加强集文件已归还至公共集！")

#读取初始版本号
def read_file_content(path, filename):

    # 拼接完整的文件路径
    full_path = f"{path}/{filename}"

    # 使用'with'语句打开文件，确保文件正确关闭
    with open(full_path, 'r', encoding='utf-8') as file:
        # 读取文件内容
        content = file.read()

        # 返回文件内容
    return content

#将上个版本写入新版本

def load_pickle(file_path):
    """加载pickle文件"""
    with open(file_path, 'rb') as file:
        return pickle.load(file)


def save_pickle(data, file_path):
    """保存数据到pickle文件"""
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


def merge_data(dict1, dict2):
    """合并两个字典中的列表"""
    merged_dict = {}
    for key in dict1.keys():
        if key in dict2:
            merged_dict[key] = dict1[key] + dict2[key]
        else:
            merged_dict[key] = dict1[key]
            # 考虑到dict2中可能有dict1中没有的键，我们也需要添加这些
    for key in dict2.keys():
        if key not in merged_dict:
            merged_dict[key] = dict2[key]
    return merged_dict


def merge_and_save_pkl(pkl_dir, pkl1_name, pkl2_name):

    # 构建文件路径
    file_path_1 = os.path.join(pkl_dir, f"{pkl1_name}")
    file_path_2 = os.path.join(pkl_dir, f"{pkl2_name}")

    # 加载两个pkl文件
    data_1 = load_pickle(file_path_1)
    data_2 = load_pickle(file_path_2)

    # 合并数据
    merged_data = merge_data(data_1, data_2)

    # 获取当前时间并格式化
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d_%H%M%S")

    # 构建新文件名（基于pkl2_name但添加时间戳）
    new_file_name = f"{pkl2_name}"
    new_file_path = os.path.join(pkl_dir, new_file_name)

    # 保存合并后的数据
    save_pickle(merged_data, new_file_path)

    print(f"pkl信息已更新到 {new_file_path}.pkl")



    #获取pkl
def huoqu_pkl(root,save_root,pklname):
    img_train = os.listdir(os.path.join(root, "images/train"))
    img_val = os.listdir(os.path.join(root, "images/val"))
    label_train = os.listdir(os.path.join(root, "labels/train"))
    label_val = os.listdir(os.path.join(root, "labels/val"))

    os.makedirs(save_root, exist_ok=True)
    # 创建一个字典来存储所有的数据集
    all_datasets = {
        'img_train': img_train,
        'img_val': img_val,
        'label_train': label_train,
        'label_val': label_val
    }

    # 生成 .pkl 文件的完整路径
    save_path = os.path.join(save_root, pklname)

    # 使用 with 语句和 pickle.dump 将 all_datasets 字典序列化到文件中
    with open(save_path, 'wb') as f:
        pickle.dump(all_datasets, f)

    print(f"加强集数据已保存到 {pklname}")



def organize_datasets(common_set_path, pkl_file_path, pkl_filename, augmented_set_path):
    # 加载pickle文件
    with open(os.path.join(pkl_file_path, pkl_filename), 'rb') as f:
        all_datasets = pickle.load(f)

    # 定义加强集内部的路径
    augmented_images_train_dir = os.path.join(augmented_set_path, 'images', 'train')
    augmented_images_val_dir = os.path.join(augmented_set_path, 'images', 'val')
    augmented_labels_train_dir = os.path.join(augmented_set_path, 'labels', 'train')
    augmented_labels_val_dir = os.path.join(augmented_set_path, 'labels', 'val')

    # 确保加强集的目录存在
    for dir_path in [augmented_images_train_dir, augmented_images_val_dir, augmented_labels_train_dir,
                     augmented_labels_val_dir]:
        os.makedirs(dir_path, exist_ok=True)

    print("根据PKL 文件，开始同步数据集······")
    # 同步每个子集
    for subset_name, files_list in all_datasets.items():
        if subset_name.startswith('img_'):
            augmented_dir = augmented_images_train_dir if 'train' in subset_name else augmented_images_val_dir
            # 公共集不需要特定目录，所以直接使用common_set_path
            common_files_dir = common_set_path
        elif subset_name.startswith('label_'):
            augmented_dir = augmented_labels_train_dir if 'train' in subset_name else augmented_labels_val_dir
            # 同样，公共集不需要特定目录
            common_files_dir = common_set_path

        # 获取加强集中现有的文件名
        existing_files = set(os.listdir(augmented_dir))
        # pickle文件中需要的文件名
        needed_files = set(files_list)
        

        # 将缺失的文件从公共集复制到加强集
        missing_files = needed_files - existing_files
        for file_name in tqdm(missing_files, desc=f"将缺失的文件从公共集复制到加强集： {subset_name}"):
            source_path = os.path.join(common_files_dir, file_name)
            destination_path = os.path.join(augmented_dir, file_name)
            shutil.move(source_path, destination_path)

        # 将多余的文件从加强集移回公共集（注意：这可能会覆盖公共集中的同名文件）
        extra_files = existing_files - needed_files
        for file_name in tqdm(extra_files, desc=f"多余的文件从加强集移回公共集： {subset_name}"):
            source_path = os.path.join(augmented_dir, file_name)
            destination_path = os.path.join(common_files_dir, file_name)
            # 如果不想覆盖公共集中的文件，可以添加一些检查或重命名逻辑
            shutil.move(source_path, destination_path)

    print(f"新pkl-{pkl_filename}对应加强集已生成 :{ augmented_set_path}")

#清理指定版本以上文件
def clean_pkl_files(folder_path, latest_version_file_path, past_pklname):
    # 使用正则表达式匹配版本号（假设版本号形如x.y）
    match = re.search(r'V(\d+\.\d+)', past_pklname)
    if match:
        version = match.group(1)
        print(f'pkl已更新至{version}版本')
    else:
        print("未找到版本号")
    version_file_path = os.path.join(folder_path, latest_version_file_path)
    # 确保提供的文件夹路径是存在的
    if not os.path.isdir(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

        # 定义一个函数来比较版本号

    def compare_versions(v1, v2):
        # 简化处理，仅支持形如 x.y 的版本号
        parts1 = v1.split('.')
        parts2 = v2.split('.')
        # 逐部分比较
        for p1, p2 in zip(parts1, parts2):
            if int(p1) > int(p2):
                return 1
            elif int(p1) < int(p2):
                return -1
                # 如果所有部分都相等，但v2有更多的部分，则认为v2是更新的版本
        if len(parts1) < len(parts2):
            return -1
        return 0

        # 正则表达式匹配文件名中的版本号

    version_pattern = re.compile(r'V(\d+\.\d+)')

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.pkl'):
            match = version_pattern.search(filename)
            if match:
                file_version = match.group(1)
                # 比较版本号
                if compare_versions(file_version, version) > 0:
                    # 删除版本号大于给定版本号的.pkl文件
                    os.remove(os.path.join(folder_path, filename))
                    print(f"Deleted: {filename}")

                    # 清空或覆盖latest_version.txt文件的内容
    write_version(version_file_path, version)



def find_common_filenames(base_path):
    # 定义子文件夹名称
    subdirs = ['images', 'labels']
    # 定义子子文件夹名称
    subsets = ['train', 'val']

    # 存储结果的字典
    results = {}

    for subdir in subdirs:
        subdir_path = os.path.join(base_path, subdir)
        # 初始化存储当前subdir下子集的文件名集合
        results[subdir] = {subset: set() for subset in subsets}

        # 遍历子集
        for subset in subsets:
            subset_path = os.path.join(subdir_path, subset)
            # 确保子集文件夹存在
            if os.path.isdir(subset_path):
                # 遍历子集文件夹中的所有文件
                for filename in os.listdir(subset_path):
                    # 假设我们只关心文件名，不考虑扩展名
                    # 如果需要包含扩展名，可以直接使用filename
                    # 这里我们使用os.path.splitext(filename)[0]来获取不带扩展名的文件名
                    # 但为了简单起见，我们直接使用filename
                    results[subdir][subset].add(filename)

                    # 找出相同文件名
    for subdir in subdirs:
        for subset in subsets:
            # 假设我们只关心与另一个子集相同的文件名
            # 这里我们简单地打印出来，但你可以根据需要修改这部分
            other_subset = 'val' if subset == 'train' else 'train'
            common_files = results[subdir][subset].intersection(results[subdir][other_subset])
            print(f"在 {subdir}/{subset} 中与 {subdir}/{other_subset} 相同的文件名有：{common_files}")



#清空公共集
def empty_folder(folder_path):
    """
    清空指定文件夹及其所有子文件夹和文件。
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

#生成新pkl执行函数
def process_and_organize_data(path,project_name, pkl_path, source_folder, temp, aug_path , istrain, methods,Aug_methods, Aug_nums, mask_labels, count, past_pklname):

    # 生成加强集项目结构
    directories = create_project_structure(temp)
    mask_save_dir = directories[0]

    # 调用封装的函数处理并增强数据
    process_and_augment_data(path, temp, Aug_methods, Aug_nums, mask_labels, count, istrain)

    # 获取新料pkl并命名
    old_name, pklname = create_new_pkl(project_name, pkl_path)
    # if methods == 2:
    #     old_name = past_pklname
    huoqu_pkl(temp, pkl_path, pklname)  # 注意：这个函数名可能是个占位符，实际名称可能不同

    # 把新料加强后的数据全部移入公共集
    move_files_to_source_folder(temp, source_folder)

    # 删除临时文件temp
    shutil.rmtree(temp)

    # 获取当前存储版本号是否为0.1，是0.1不进行与之前版本数据合并，不是则合并
    version = float(read_file_content(pkl_path, version_file_name))
    if version == 0.1:
        pass
    else:
        merge_and_save_pkl(pkl_path, old_name, pklname)

    # 加强集与pkl文件对照，使pkl文件和aug一一对应
    organize_datasets(source_folder, pkl_path, pklname, aug_path)


# 对比较文件夹中的文件,去删除folder2中的文件
def delete_duplicate_files(folder1, folder2):
    """
    遍历folder1和folder2的子文件夹，并删除folder2中与folder1中文件名相同的文件。

    :param folder1: 第一个文件夹的路径
    :param folder2: 第二个文件夹的路径
    """
    # 创建一个集合来存储folder1中所有文件的文件名（包括子文件夹中的文件）
    files_in_folder1 = set()

    # 遍历folder1及其所有子文件夹
    for root, dirs, files in os.walk(folder1):
        for file in files:
            # 使用os.path.relpath获取相对于folder1的相对路径（可选，但这里我们只需要文件名）
            # files_in_folder1.add(os.path.relpath(os.path.join(root, file), folder1))
            # 但为了简化，我们只添加文件名（不包括路径）
            files_in_folder1.add(file)

            # 遍历folder2及其所有子文件夹
    for root, dirs, files in os.walk(folder2):
        for file in list(files):  # 注意这里我们使用list(files)，因为我们要在遍历过程中修改files
            if file in files_in_folder1:
                # 构建要删除的文件的完整路径
                file_path = os.path.join(root, file)
                print(f"Deleting {file_path}")
                # 删除文件
                os.remove(file_path)
                # 从files列表中移除已删除的文件名，以避免后续错误（尽管在大多数情况下这不是必需的）
                files.remove(file)

def function(path, project_name, methods, other_path, output_path, istrain, Aug_methods, Aug_nums, mask_labels, count, past_pklname):
    #创建目录
    if not os.path.exists(other_path):
        os.makedirs(other_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    temp, pkl_path, source_folder = create_temp(other_path)
    if methods == 0:
        process_and_organize_data(path, project_name, pkl_path, source_folder, temp, output_path, istrain,  methods, Aug_methods, Aug_nums, mask_labels, count, past_pklname)
    elif methods == 1:
        shutil.rmtree(temp)
        clean_pkl_files(pkl_path, version_file_name, past_pklname)
        organize_datasets(source_folder, pkl_path, past_pklname, output_path)
    else:
        print("methods的值必须是0或1")

    # 显示加强集里各文件数量#
    count_files_in_dirs(output_path,source_folder)
    find_common_filenames(output_path)


# 加强集各目录和公共集数量计算
def count_files_in_dirs(base_path, source_folder):
    print("统计加强集各目录和公共集数量")
    # 定义要检查的子目录列表
    dirs_to_check = [
        ('images/train', os.path.join(base_path, 'images', 'train')),
        ('images/val', os.path.join(base_path, 'images', 'val')),
        ('labels/train', os.path.join(base_path, 'labels', 'train')),
        ('labels/val', os.path.join(base_path, 'labels', 'val')),
        ('公共集文件数', source_folder)
    ]

    # 遍历定义的目录并统计文件数量
    for dir_name, path in dirs_to_check:
        file_count = len(glob.glob(os.path.join(path, '*')))
        print(f"Number of files in {dir_name}: {file_count}")


if __name__ == '__main__':
    # 需加强数据集路
    path = r'D:\MeMs\1\test\m1_dark'
    # 保存pkl文件夹，临时文件夹，公共集路径
    other_path = r'D:\MeMs\1\test\pkl'
    # 项目名称
    project_name = 'MZ'
    
    # 输出数据集位置+在对应项目名下
    all_path = r'D:\MeMs\1\test\station1'

    # 设置数据增强方法和参数
    Aug_methods = ['vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise']
    Aug_nums = [0, 1, 2]
    mask_labels = []
    count = 3

    # 是否将原图存入 train
    istrain = True

    # 选择运行方式:
    # methods = 0:执行加入文件生成最新版pkl生成对应数据集
    # methods = 1:恢复到指定pkl文件past_pklname
    methods = 0
    past_pklname = "240922_MZ_V0.1.pkl"

    origin_path = os.path.join(other_path, project_name)
    output_path = os.path.join(all_path,  project_name)
    function(path, project_name, methods, origin_path, output_path, istrain, Aug_methods, Aug_nums, mask_labels, count, past_pklname)

