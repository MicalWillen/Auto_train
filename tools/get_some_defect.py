import os
import shutil
from tqdm import tqdm
fileroot = r"/data0/Colin/yolov5/datasets/CELL/0111/CELL_org_data_forClean/station9"
picked_root = r"/data0/Colin/yolov5/datasets/CELL/0111/CELL_org_data_forClean/station9_0"
os.makedirs(picked_root,exist_ok=True)
filenames = []
defect_type = 0
for file in os.listdir(fileroot):
    if file.endswith(".txt"):
        filenames.append(file)

for txtfile in tqdm(filenames):
    try:
        with open(os.path.join(fileroot,txtfile),"r") as f:
            anns = f.read().splitlines()
            indicator = 0
            for ann in anns:
                # if ann.startswith(str(defect_type)):
                #     indicator =1
                if ann.split(" ")[0] == str(defect_type):
                    indicator=1
        if indicator == 1:
            # shutil.copy(os.path.join(fileroot,txtfile),os.path.join(picked_root,txtfile))
            # shutil.copy(os.path.join(fileroot,txtfile[:-4]+".bmp"),os.path.join(picked_root,txtfile[:-4]+".bmp"))

            if os.path.exists(os.path.join(fileroot, txtfile[:-4] + ".jpg")):
                shutil.move(os.path.join(fileroot, txtfile[:-4] + ".jpg"),
                            os.path.join(picked_root, txtfile[:-4] + ".jpg"))
            else:
                shutil.move(os.path.join(fileroot, txtfile[:-4] + ".bmp"),
                            os.path.join(picked_root, txtfile[:-4] + ".bmp"))
            shutil.move(os.path.join(fileroot,txtfile),os.path.join(picked_root,txtfile))

    except Exception as e:
        # shutil.copy(os.path.join(fileroot,txtfile[:-4]+".bmp"),os.path.join(picked_root,txtfile[:-4]+".bmp"))
        print(e)
