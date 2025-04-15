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
            s = []  # 如果需要遮盖，创建一个空列表
            for i in range(1, len(new_info), 2):
                b = []
                for tmp in new_info[i:i + 2]:
                    if tmp != '':
                        b.append(float(tmp))  # x,y/w,h
                if b != []:
                    s.append(b[0])
                    s.append(b[1])
            s = np.array(s)
            x1 = int((float(s[0]) - float(s[2]) / 2) * width)  # x_center - width/2 将归一化之后的数据变回原来的大小
            y1 = int((float(s[1]) - float(s[3]) / 2) * height)  # y_center - height/2
            x2 = int((float(s[0]) + float(s[2]) / 2) * width)  # x_center + width/2
            y2 = int((float(s[1]) + float(s[3]) / 2) * height)  # y_center + height/2
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 0), thickness=-1)  # BGR
    return img


def merger_select_label(ori, save, b_lables):
    ori_file_handle = open(ori)

    cnt_info = ori_file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]
    new_infos = []
    for info in new_cnt_info:
        if int(info[0]) in b_lables:
            continue
        new_info = []
        for i in range(len(info)):
            new_info.append(info[i])
        new_infos.append(new_info)
    with open(save, 'a', encoding='utf-8') as new_file_obj:
        for k in range(len(new_infos)):
            for k_k in range(len(new_infos[k])):
                new_file_obj.write('{} '.format(new_infos[k][k_k]))
            new_file_obj.write('\n')
    print('write file {} to file {} merge complete!'.format(ori, save))


def Gaussnoise_func(image, mean=0, var=0.005):
    '''
    添加高斯噪声
    mean : 均值
    var : 方差
    '''
    image = np.array(image / 255, dtype=float)  # 将像素值归一
    noise = np.random.normal(mean, var ** 0.5, image.shape)  # 产生高斯噪声
    out = image + noise  # 直接将归一化的图片与噪声相加

    '''
    将值限制在(-1/0,1)间，然后乘255恢复
    '''
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.

    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out * 255)
    return out


def draw_txt_gaussian_mask(image, txt_path, mask_label, img_path):
    height, width = image.shape[0], image.shape[1]
    img = np.array(image)
    img2 = np.zeros((height, width, 3), dtype='uint8')
    img3 = np.zeros((height, width, 3), dtype='uint8')

    # 在原图上画出需要添加噪声的黑色区域
    file_handle = open(txt_path)
    cnt_info = file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]

    for new_info in new_cnt_info:
        temp_label = int(new_info[0])
        if mask_label == temp_label:
            s = []
            for i in range(1, len(new_info), 2):
                b = []
                for tmp in new_info[i:i + 2]:
                    if tmp != '':
                        b.append(float(tmp))
                if b != []:
                    s.append(b[0])
                    s.append(b[1])
            s = np.array(s)
            x1 = int((float(s[0]) - float(s[2]) / 2) * width)  # x_center - width/2
            y1 = int((float(s[1]) - float(s[3]) / 2) * height)  # y_center - height/2
            x2 = int((float(s[0]) + float(s[2]) / 2) * width)  # x_center + width/2
            y2 = int((float(s[1]) + float(s[3]) / 2) * height)  # y_center + height/2
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 0), thickness=-1)
            cv2.rectangle(img3, (x1, y1), (x2, y2), color=(1, 1, 1), thickness=-1)

    img_temp = Image.open(img_path)
    stat = ImageStat.Stat(img_temp)
    # print('mean: {}; variance: {}'.format(float(stat.mean[0]), float(stat.stddev[0])))

    img_gaussian = Gaussnoise_func(img2, float(stat.mean[0]), float(stat.stddev[0]) ** 2)
    img_out = img + img3 * img_gaussian

    return img_out
