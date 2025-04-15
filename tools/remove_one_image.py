import os
root = "/data0/wtw/yolov5_2/datasets/CELL/CELL_station3/m12d22_station3_v63_cleanedDefect3_JiZhuFuShi"
filename = "12_001CE0B000000EDCJ0407266-11_001CE0B000000EDCJ0407250-Station3-6-0.bmp"
os.remove(os.path.join(root,"images/train",filename))
os.remove(os.path.join(root,"images/train",f"horizational_{filename}"))
os.remove(os.path.join(root,"images/val",f"rotate180_{filename}"))
os.remove(os.path.join(root,"images/val",f"vertical_{filename}"))

os.remove(os.path.join(root,"labels/train",filename[:-4]+".txt"))
os.remove(os.path.join(root,"labels/train",f"horizational_{filename[:-4]}.txt"))
os.remove(os.path.join(root,"labels/val",f"rotate180_{filename[:-4]}.txt"))
os.remove(os.path.join(root,"labels/val",f"vertical_{filename[:-4]}.txt"))
print("done")