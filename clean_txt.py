import os
from tqdm import tqdm
# 挑选过数据集中可能会control shift d 删除一些样本 但是会留txt文件 这个脚本用于删除多余的txt文件
root = r"/home2/item/FX/down/每日存/0619"
jpg_namelist = []
txt_namelist = []

for filename in tqdm(os.listdir(root)):
    if filename.endswith(".jpg") or filename.endswith(".bmp")or filename.endswith(".png"):
        jpg_namelist.append(filename[:-4])
    if filename.endswith(".txt"):
        txt_namelist.append(filename[:-4])
if len(jpg_namelist)==0:
    raise Exception("jpg Namelist empty")
for txt_filename in txt_namelist:
    if txt_filename not in jpg_namelist:
        os.remove(os.path.join(root,txt_filename+".txt"))
