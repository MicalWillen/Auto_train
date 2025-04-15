# import json
# import glob
# import os

# import cv2
# import numpy as np
# #用于将labelme标注数据转化为txt标注
# json_path = r"D:\FR\test\crush1"; #此处填写存放json文件的地址
# labels = ['4','5']#此处填写你标注的标签名称
# json_files = glob.glob(json_path + "/*.json")

# for json_file in json_files:
#     print(json_file)
#     f = open(json_file)
#     json_info = json.load(f)
#     # print(json_info.keys())
#     img = cv2.imread(os.path.join(json_path, json_info["imagePath"]))
#     height, width, _ = img.shape

#     np_w_h = np.array([[width, height]], np.int32)
#     txt_file = json_file.replace(".json", ".txt")
#     f = open(txt_file, "a")
#     for point_json in json_info["shapes"]:
#         txt_content = ""
#         np_points = np.array(point_json["points"], np.int32)
#         norm_points = np_points / np_w_h
#         norm_points_list = norm_points.tolist()
#         print()
#         if point_json['label'] == labels[0]:
#             txt_content += "0 " + " ".join([" ".join([str(cell[0]), str(cell[1])]) for cell in norm_points_list]) + "\n"
#         elif point_json['label'] == labels[1]:
#             txt_content += "1 " + " ".join([" ".join([str(cell[0]), str(cell[1])]) for cell in norm_points_list]) + "\n"

#         f.write(txt_content)

import json
import glob
import os
import cv2
import numpy as np

# 用于将 LabelMe 标注数据转换为 txt 标注
json_path = r"D:\FR\test\crush1\3"  # 此处填写存放 JSON 文件的地址

# 获取所有 JSON 文件
json_files = glob.glob(os.path.join(json_path, "*.json"))

# 自动提取所有可能的标签
labels_set = set()
for json_file in json_files:
    with open(json_file, 'r') as f:
        json_info = json.load(f)
        for shape in json_info.get("shapes", []):
            labels_set.add(shape.get("label", ""))
labels = sorted(labels_set)

print(f"Detected labels: {labels}")

for json_file in json_files:
    print(f"Processing: {json_file}")

    # 加载 JSON 文件
    with open(json_file, 'r') as f:
        json_info = json.load(f)

    # 读取图像信息
    img_path = os.path.join(json_path, json_info.get("imagePath", ""))
    img = cv2.imread(img_path)

    if img is None:
        print(f"Image not found or cannot be loaded: {img_path}")
        continue

    height, width, _ = img.shape
    np_w_h = np.array([width, height], dtype=np.float32)

    # 打开目标 txt 文件
    txt_file = json_file.replace(".json", ".txt")
    with open(txt_file, "w") as txt_f:
        # 遍历 JSON 中的 shapes
        for shape in json_info.get("shapes", []):
            label = shape.get("label", "")
            points = np.array(shape.get("points", []), dtype=np.float32)

            # 正常化坐标点
            norm_points = points / np_w_h

            # 根据标签匹配并生成内容
            if label in labels:
                class_id = label
                points_str = " ".join([f"{x:.6f} {y:.6f}" for x, y in norm_points])
                txt_content = f"{class_id} {points_str}\n"
                txt_f.write(txt_content)

    print(f"Saved: {txt_file}")
