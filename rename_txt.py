# modify labels with area
import cv2
import os
import numpy as np
from tqdm import tqdm

def Cal_LW_Ratio(x1, y1, x2, y2):
    L = x2 - x1
    R = y2 - y1
    if L >= R:
        ratio = R/L
    else:
        ratio = L/R
    return ratio


envpath = '/data/xx/xx/venv/lib/python3.6/site-packages/cv2/qt/plugins/platforms'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = envpath

img_dir = r'D:\Document\文档\WXWork\1688855780506589\Cache\File\2024-09\12'
save_dir = r'D:\Document\文档\WXWork\1688855780506589\Cache\File\2024-09\13'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
files = os.listdir(img_dir)


for file in tqdm(files):
    if '.txt' not in file:
        continue
    filename = file[0:-4]
    # img_name = file
    txt_name = filename + '.txt'
    # pic = os.path.join(img_dir, img_name)
    txt = os.path.join(img_dir, txt_name)
    # if not os.path.exists(txt):
    #     print('{} not found'.format(pic))
    #     continue


    # img = cv2.imdecode(np.fromfile(pic, dtype=np.uint8), cv2.IMREAD_COLOR)
    # height, width, _ = img.shape

    file_handle = open(txt)
    cnt_info = file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]

    color_map = {"0": (0, 255, 255), "1": (255, 0, 255), "2": (255, 255, 0), "3": (255, 0, 0), '4': (255, 0, 0),
                 '5': (255, 255, 255), '6': (255, 0, 255), '7': (0, 0, 255), '8': (0, 0, 0)}

    new_labels = []
    for new_info in new_cnt_info:
        s = []
        s.append(new_info[0])
        for i in range(1, len(new_info), 2):
            b = []
            for tmp in new_info[i:i + 2]:
                if tmp != '':
                    b.append(float(tmp))
            # b = [float(tmp) for tmp in new_info[i:i + 2]]
            if b != []:
                s.append(b[0])
                s.append(b[1])
        # cv2.polylines(img, [np.array(s, np.int32)], True, color_map.get(new_info[0]), thickness=1)
        s = np.array(s)
        if s[0] == '46' or s[0] == '47' or s[0] == '48' or s[0] == '49':
            s[0] = '50'
        # elif s[0] == '10':
        #     s[0] = '1'

        s_new = list(s)
        new_labels.append(list(s_new))
        with open(os.path.join(save_dir, txt_name), 'w', encoding='utf-8') as new_file_obj:
            for k in range(len(new_labels)):
                for k_k in range(len(new_labels[k])):
                    new_file_obj.write('{} '.format(new_labels[k][k_k]))
                new_file_obj.write('\n')