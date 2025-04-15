import numpy as np
import cv2
import os
from utils_old import draw_txt_mask, merger_select_label
from tqdm import tqdm

if __name__ == '__main__':
    # lab_img_dir存储标注，如果没有存储路径会自动创建
    # 使用opencv读取图片路径不能有中文
    mask_labels = [50]
    ori_img_dir = r'D:\A\TC\TC_datasets'
    txt_dir = ori_img_dir
    save_dir = r'D:\A\TC\s6d'

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    files = os.listdir(ori_img_dir)
    for file in tqdm(files):
        if 'txt' in file:
            continue

        # 通过img名字在txt路径下找txt文件
        if not os.path.exists(os.path.join(txt_dir, file[:-4] + '.txt')):
            print('{} has not label'.format(file))
            continue

        img = cv2.imread(os.path.join(ori_img_dir, file))
        img_mask = draw_txt_mask(img, os.path.join(txt_dir, file[:-4] + '.txt'), mask_labels)

        cv2.imwrite(os.path.join(save_dir, file), img_mask)  # 保存被遮盖的图片

        filename = file[:-4]
        ori_txt = filename + '.txt'
        save_txt = filename + '.txt'

        ori_txt = os.path.join(txt_dir, ori_txt)
        save_txt = os.path.join(save_dir, save_txt)

        merger_select_label(ori_txt, save_txt, mask_labels)
