from ast import Delete
from datetime import datetime, timedelta
import re
import os
from tkinter import END
from tqdm import tqdm
import shutil
import subprocess
import numpy as np


def mk_picture_class(file_path):
    d6 = "6_dark"
    d3 = "3_dark"
    l3 = "3_light"
    l6 = "6_light"
    d9 = "9_dark"
    d1 = "1_dark"
    j3 = "3_jizu"
    l7 = "7_light"
    d7 = "7_dark"
    root = file_path
    for filename in tqdm(os.listdir(root)):
        if 'Station6' in filename:
            match = re.findall(r'\d+', filename)[-1]
            if match == '1':
                if not os.path.exists(os.path.join(root, d6)):
                    os.makedirs(os.path.join(root, d6))
                shutil.move(os.path.join(root, filename), os.path.join(root, d6))
            if match == '0':
                if not os.path.exists(os.path.join(root, l6)):
                    os.makedirs(os.path.join(root, l6))
                shutil.move(os.path.join(root, filename), os.path.join(root, l6))

    for filename in tqdm(os.listdir(root)):
        if 'Station3' in filename:
            match = re.findall(r'\d+', filename)[-1]
            if match == '1':
                if not os.path.exists(os.path.join(root, d3)):
                    os.makedirs(os.path.join(root, d3))
                shutil.move(os.path.join(root, filename), os.path.join(root, d3))
            if match == '0':
                if not os.path.exists(os.path.join(root, l3)):
                    os.makedirs(os.path.join(root, l3))
                shutil.move(os.path.join(root, filename), os.path.join(root, l3))

    for filename in tqdm(os.listdir(root)):
        if 'Station1' in filename:
            if not os.path.exists(os.path.join(root, d1)):
                os.makedirs(os.path.join(root, d1))
            shutil.move(os.path.join(root, filename), os.path.join(root, d1))

    for filename in tqdm(os.listdir(root)):
        if 'Station9' in filename:
            if not os.path.exists(os.path.join(root, d9)):
                os.makedirs(os.path.join(root, d9))
            shutil.move(os.path.join(root, filename), os.path.join(root, d9))
    for filename in tqdm(os.listdir(root)):
        if 'Station8' in filename:
            if not os.path.exists(os.path.join(root, j3)):
                os.makedirs(os.path.join(root, j3))
            shutil.move(os.path.join(root, filename), os.path.join(root, j3))
    for filename in tqdm(os.listdir(root)):
        if 'Station7' in filename:
            match = re.findall(r'\d+', filename)[-2]
            if len(re.findall(r'\d+', filename))!=8:
                if match == '1':
                    if not os.path.exists(os.path.join(root, d7)):
                        os.makedirs(os.path.join(root, d7))
                    shutil.move(os.path.join(root, filename), os.path.join(root, d7))
                if match == '0':
                    if not os.path.exists(os.path.join(root, l7)):
                        os.makedirs(os.path.join(root, l7))
                    shutil.move(os.path.join(root, filename), os.path.join(root, l7))
    # for filename in tqdm(os.listdir(root)):
    #         match = re.findall(r'\d+', filename)[-1]
    #         if match == '1':
    #             if not os.path.exists(os.path.join(root, "light")):
    #                 os.makedirs(os.path.join(root, "light"))
    #             shutil.move(os.path.join(root, filename), os.path.join(root, d7))
    #         if match == '0':
    #             if not os.path.exists(os.path.join(root, "dark")):
    #                 os.makedirs(os.path.join(root, "dark"))
    #             shutil.move(os.path.join(root, filename), os.path.join(root, l7))

file_path = r'D:\CELL\每日存\0606\大面\软质检成硬质'
mk_picture_class(file_path)    
