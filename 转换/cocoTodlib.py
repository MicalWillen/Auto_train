import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

from tqdm import tqdm  # 修复导入问题

def convert_coco_to_xml(coco_file, output_file):
    # 检查文件是否存在
    if not os.path.exists(coco_file):
        print(f"文件 {coco_file} 不存在")
        return

    # 读取 COCO JSON 文件
    with open(coco_file, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)

    # 创建 XML 根节点
    dataset = ET.Element('dataset')
    name = ET.SubElement(dataset, 'name')
    name.text = "COCO Dataset"
    comment = ET.SubElement(dataset, 'comment')
    comment.text = "Converted from COCO format"
    images = ET.SubElement(dataset, 'images')

    # 遍历图像信息
    for image in tqdm(coco_data.get('images', [])):  # 修复 tqdm 用法
        image_node = ET.SubElement(images, 'image', file=image['file_name'])
        width = image.get('width', 0)
        height = image.get('height', 0)

        # 遍历标注信息
        for annotation in coco_data.get('annotations', []):
            if annotation['image_id'] == image['id']:
                bbox = annotation['bbox']
                x1, y1, bw, bh = bbox
                x2 = x1 + bw
                y2 = y1 + bh

                box = ET.SubElement(image_node, 'box', top=str(int(y1)), left=str(int(x1)),
                                    width=str(int(bw)), height=str(int(bh)))
                label = ET.SubElement(box, 'label')
                label.text = str(annotation['category_id'])

    # 格式化 XML 并保存到文件
    rough_string = ET.tostring(dataset, encoding='utf-8', method='xml')
    reparsed = minidom.parseString(rough_string)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reparsed.toprettyxml(indent="  "))

# 示例调用
convert_coco_to_xml(
    '/home2/temp/zhiyuan_objv2_val.json',  # COCO格式JSON文件路径
    '/home2/temp/zhiyuan_objv2_val1.xml'    # 输出XML文件路径
)