import os
import xml.etree.ElementTree as ET
import cv2

def convert_xml_to_yolo_detection(xml_path, output_folder, image_folder):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image in root.findall('./images/image'):
        filename = image.get('file')
        image_name = os.path.basename(filename)
        txt_name = os.path.splitext(image_name)[0] + '.txt'
        txt_path = os.path.join(output_folder, txt_name)

        image_path = os.path.join(image_folder, image_name)
        if not os.path.exists(image_path):
            print(f"Warning: image not found: {image_path}")
            continue

        img = cv2.imread(image_path)
        if img is None:
            print(f"Warning: failed to read image: {image_path}")
            continue
        h, w = img.shape[:2]

        lines = []
        for box in image.findall('box'):
            label = box.find('label')
            class_id = label.text if label is not None else '0'

            # 获取边界框坐标
            x_min = float(box.get('left'))
            y_min = float(box.get('top'))
            x_max = float(box.get('left')) + float(box.get('width'))
            y_max = float(box.get('top')) + float(box.get('height'))

            # 归一化坐标
            x_center = ((x_min + x_max) / 2) / w
            y_center = ((y_min + y_max) / 2) / h
            bbox_width = (x_max - x_min) / w
            bbox_height = (y_max - y_min) / h

            line = f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
            lines.append(line)

        # 写入（即使没有标注也生成空文件）
        with open(txt_path, 'w') as f:
            f.write('\n'.join(lines))

# 使用示例
convert_xml_to_yolo_detection(
    '/home2/temp/fangdiaoqi/fangdiaoqi/substacted_savetocurrentdirfast.xml',   # XML 文件
    '/home2/temp/fangdiaoqi/fangdiaoqi/txt_detection',      # 输出 txt 文件夹
    '/home2/temp/fangdiaoqi/fangdiaoqi/substacted_savetocurrentdirfast'        # 对应图像文件夹
)