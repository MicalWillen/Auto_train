import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2

def convert_yolo_box_to_xml(image_folder, txt_folder, output_file):
    dataset = ET.Element('dataset')
    name = ET.SubElement(dataset, 'name')
    comment = ET.SubElement(dataset, 'comment')
    images = ET.SubElement(dataset, 'images')

    image_list = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for image_name in image_list:
        image_path = os.path.join(image_folder, image_name)
        txt_name = os.path.splitext(image_name)[0] + '.txt'
        txt_path = os.path.join(txt_folder, txt_name)

        if not os.path.exists(txt_path):
            open(txt_path, 'w').close()  # 创建空的txt文件
            continue  # 空图像跳过

        img = cv2.imread(image_path)
        if img is None:
            continue
        h, w = img.shape[:2]

        image = ET.SubElement(images, 'image', file=os.path.join(os.path.basename(image_folder), image_name))

        with open(txt_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            class_id, cx, cy, bw, bh = parts
            cx, cy, bw, bh = float(cx), float(cy), float(bw), float(bh)

            x1 = int((cx - bw / 2) * w)
            y1 = int((cy - bh / 2) * h)
            x2 = int((cx + bw / 2) * w)
            y2 = int((cy + bh / 2) * h)

            x1, y1 = max(x1, 0), max(y1, 0)
            x2, y2 = min(x2, w), min(y2, h)

            box = ET.SubElement(image, 'box', top=str(y1), left=str(x1),
                                width=str(x2 - x1), height=str(y2 - y1))
            label = ET.SubElement(box, 'label')
            label.text = class_id

    rough_string = ET.tostring(dataset, encoding='utf-8', method='xml')
    reparsed = minidom.parseString(rough_string)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reparsed.toprettyxml(indent="  "))

# 示例调用
convert_yolo_box_to_xml(
    '/home/ps/AB/framework/rf-detr-develop/pridect/23/output_images',  # 图像路径
    '/home/ps/AB/framework/rf-detr-develop/pridect/23/output_labels',  # YOLO格式txt路径
    '/home/ps/AB/framework/rf-detr-develop/pridect/23/output_labels.xml'  # 输出XML
)
