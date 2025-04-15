import os
from tqdm import tqdm
def walkfolder(srcdir):
    index = 1
    max_index = 0
    pbar = tqdm(os.walk(srcdir, True))
    for root, dirs, files in pbar:
        for file in files:
            if file.endswith(".txt") and not file.startswith("classes"):
                with open(os.path.join(root,file),"r") as f:
                    lines = f.readlines()
                    for line in lines:
                        index = int(line.split(" ")[0])
                        if index>max_index or index==max_index:
                            print(f"{index},{file}")
                            max_index = index


walkfolder(r"/tmp/test_Colin/yolov5-master/yolov5-7.0/datasets/newjizhufushi/labels/val")