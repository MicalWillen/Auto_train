import numpy as np
import cv2
import os
from PIL import Image, ImageStat


# Draw block are with special label
def draw_txt_mask(img, txt_path, mask_labels):
    image_size = img.shape
    height, width = image_size[:2]

    file_handle = open(txt_path)
    cnt_info = file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]

    for new_info in new_cnt_info:
        temp_label = int(new_info[0])
        if temp_label in mask_labels:
            s = new_info[1:]
            s = np.array(s)
            x1 = int((float(s[0]) - float(s[2]) / 2) * width)  # x_center - width/2 将归一化之后的数据变回原来的大小
            y1 = int((float(s[1]) - float(s[3]) / 2) * height)  # y_center - height/2
            x2 = int((float(s[0]) + float(s[2]) / 2) * width)  # x_center + width/2
            y2 = int((float(s[1]) + float(s[3]) / 2) * height)  # y_center + height/2
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=-1)  # BGR
    return img


# 写新标签
def merger_select_label(ori, save, b_lables): # 原标签，现标签，遮盖的标签
    ori_file_handle = open(ori)

    cnt_info = ori_file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]
    new_infos = []
    for info in new_cnt_info:
        if int(info[0]) in b_lables:
            continue
        new_info = info
        new_info = np.array(new_info)
        new_infos.append(new_info)
    with open(save, 'a', encoding='utf-8') as new_file_obj:
        for k in range(len(new_infos)):  # 判断框的数量写几行
            for k_k in range(len(new_infos[k])):  # c,x,y,w,h 每一行的内容
                new_file_obj.write(f'{new_infos[k][k_k]}')
            new_file_obj.write('\n')  # 写完一行之后换行
    print('write file {} to file {} merge complete!'.format(ori, save))
