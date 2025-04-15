import os
import shutil
from tqdm import tqdm
# file_root = "/Users/dinnar/Desktop/cell_project/worker200/dataset/station3/v6/m07d11_station3_dark_v6/labels/train"
##3_dark
# file_root = "/data0/Colin/yolov5/datasets/CELL/0111/CELL/m01d06_station3_v67_cleanedDefect3_JiZhuFuShi"
# save_root = "/data0/Colin/yolov5/datasets/CELL/0111/CELL_org_data_forClean/station3_dark"
# #7_light
# file_root = "/data0/Colin/yolov5/datasets/CELL/0111/CELL/m05d09_station7_light_v1"
# save_root = "/data0/Colin/yolov5/datasets/CELL/0111/CELL_org_data_forClean/station7_light"
# #9_light
# file_root = "/data0/Colin/yolov5/datasets/CELL/0111/CELL/m01d06_station9_v48"
# save_root = "/data0/Colin/yolov5/datasets/CELL/0111/CELL_org_data_forClean/station9_light"
#3_jizu
file_root = r"D:\FR\clean\WX1128zm"
save_root = r"D:\FR\clean\1\WX1128zm"
os.makedirs(save_root,exist_ok=True)
file_roots = [os.path.join(file_root,"images/val"),os.path.join(file_root,"labels/val"),os.path.join(file_root,"images/train"),os.path.join(file_root,"labels/train")]
# file_roots = [os.path.join(file_root,"images/train"),os.path.join(file_root,"labels/train")]

for file_root in file_roots:
    for file in tqdm(os.listdir(file_root)):
        if "vertical" not in file and "horizontal" not in file and "rotate180" not in file and "anticlockwise90" not in file and "clockwise" not in file:
            shutil.copy(os.path.join(file_root,file),os.path.join(save_root,file))
