import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2

def convert_yolo_seg_to_xml(image_folder, txt_folder, output_file):
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
            with open(txt_path, 'w') as f:
                pass  # 创建空的txt文件

        img = cv2.imread(image_path)
        if img is None:
            continue  # 跳过无法读取的图像
        h, w = img.shape[:2]

        image = ET.SubElement(images, 'image', file=os.path.join(os.path.basename(image_folder), image_name))

        with open(txt_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 7 or len(parts) % 2 == 0:
                continue

            class_id = parts[0]
            coords = list(map(float, parts[1:]))

            xs = [int(coords[i] * w) for i in range(0, len(coords), 2)]
            ys = [int(coords[i] * h) for i in range(1, len(coords), 2)]

            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)

            box = ET.SubElement(image, 'box', top=str(ymin), left=str(xmin),
                                width=str(xmax - xmin), height=str(ymax - ymin))
            label = ET.SubElement(box, 'label')
            label.text = class_id

            for i in range(len(xs)):
                ET.SubElement(box, 'point', x=str(xs[i]), y=str(ys[i]))

    rough_string = ET.tostring(dataset, encoding='utf-8', method='xml')
    reparsed = minidom.parseString(rough_string)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reparsed.toprettyxml(indent="  "))



# 使用示例
convert_yolo_seg_to_xml(
    '/home2/item/RFDETR/jiaqi_seg/test/images/val',  # 图片路径
    '/home2/item/RFDETR/jiaqi_seg/test/labels/val',  # YOLO txt路径
    '/home2/item/RFDETR/jiaqi_seg/test/labels/val.xml'  # 输出
)
