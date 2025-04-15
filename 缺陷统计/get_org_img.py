import os
import shutil
from tqdm import tqdm


def copy_txt_files(detect_path):
    labels_dir = os.path.join(detect_path, 'labels')
    if os.path.exists(labels_dir) and os.path.isdir(labels_dir):
        for txt_file in tqdm(os.listdir(labels_dir), desc="Copying .txt files", unit="file"):
            if txt_file.endswith('.txt'):
                shutil.copy(os.path.join(labels_dir, txt_file), detect_path)


def copy_files(val_path, detect_path):
    right_dir = os.path.join(detect_path, 'right')
    revise_dir = os.path.join(detect_path, 'revise')

    os.makedirs(right_dir, exist_ok=True)
    os.makedirs(revise_dir, exist_ok=True)

    detect_txts = set([f.split('.')[0] for f in os.listdir(detect_path) if f.endswith('.txt')])

    for file_name in tqdm(os.listdir(detect_path), desc="Processing files", unit="file"):
        if file_name.endswith(('.jpg', '.png', '.bmp')):
            base_name = file_name.split('.')[0]
            ext = file_name.split('.')[1]

            if base_name in detect_txts:
                # 复制图片
                source = os.path.join(val_path, file_name)
                target = os.path.join(revise_dir, file_name)
                shutil.copy(source, target)

                # 复制对应的txt文件
                source_txt = os.path.join(val_path, f'{base_name}.txt')
                if os.path.exists(source_txt):
                    target_txt = os.path.join(revise_dir, f'{base_name}.txt')
                    shutil.copy(source_txt, target_txt)
            else:
                # 复制图片
                source = os.path.join(val_path, file_name)
                target = os.path.join(right_dir, file_name)
                shutil.copy(source, target)

                # 复制对应的txt文件
                source_txt = os.path.join(val_path, f'{base_name}.txt')
                if os.path.exists(source_txt):
                    target_txt = os.path.join(right_dir, f'{base_name}.txt')
                    shutil.copy(source_txt, target_txt)


def delete_txt_files(detect_path):
    for file_name in tqdm(os.listdir(detect_path), desc="Deleting .txt files", unit="file"):
        if file_name.endswith('.txt'):
            os.remove(os.path.join(detect_path, file_name))


def get_org_img(val_path, detect_path):
    copy_txt_files(detect_path)
    copy_files(val_path, detect_path)


if __name__ == '__main__':
    # 被检测目录
    val_path = r'D:\MeMs\每日存\1023\labeled\m1_dark'
    # 检测后目录
    detect_path = r'D:\Document\desktop\yolov5-master\yolov5-master\runs\detect\mems114'
    
    get_org_img(val_path, detect_path)

