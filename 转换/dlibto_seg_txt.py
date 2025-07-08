import os
import xml.etree.ElementTree as ET
import cv2

def convert_xml_to_yolo_seg(xml_path, output_folder, image_folder):
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

            points = box.findall('point')
            if not points:
                continue

            coords = []
            for p in points:
                x = float(p.get('x')) / w
                y = float(p.get('y')) / h
                coords.extend([f'{x:.6f}', f'{y:.6f}'])

            line = f"{class_id} " + " ".join(coords)
            lines.append(line)

        # 写入（即使没有标注也生成空文件）
        with open(txt_path, 'w') as f:
            f.write('\n'.join(lines))

# 使用示例
convert_xml_to_yolo_seg(
    '/home2/temp/fangdiaoqi/fangdiaoqi/substacted_savetocurrentdirfast.xml',   # XML 文件
    '/home2/temp/fangdiaoqi/fangdiaoqi/txt',      # 输出 txt 文件夹
    '/home2/temp/fangdiaoqi/fangdiaoqi/substacted_savetocurrentdirfast'        # 对应图像文件夹
)
