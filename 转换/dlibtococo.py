import os
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm

def convert_xml_to_coco(xml_file, output_file, image_folder):
    if not os.path.exists(xml_file):
        print(f"文件 {xml_file} 不存在")
        return

    tree = ET.parse(xml_file)
    root = tree.getroot()

    images = []
    annotations = []
    categories = []
    category_name_to_id = {}

    annotation_id = 0
    category_id_counter = 0

    # 解析 images
    for image_node in tqdm(root.findall('./images/image')):
        # 获取图像文件名,不要路径
        file_name = image_node.attrib.get('file', '').split('/')[-1]  # 只保留文件名部分
        #在图片文件夹下查找对应图片，并获取宽高
        image_path = os.path.join(image_folder, file_name)
        if not os.path.exists(image_path):
            print(f"警告: 图像文件 {file_name} 在指定的文件夹 {image_folder} 中不存在。")
            continue
        #读取图像的宽高
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                width, height = img.size
        except ImportError:
            print("PIL库未安装，无法获取图像尺寸。请安装Pillow库。")
            # 如果没有PIL库，可以手动设置宽高为0
        # width =
        # height = 0
        # 你之前的xml中没有width和height直接放在image标签属性，只有COCO中有，  
        # 如果你xml里没有，可以用0或者你自己加扩展字段。这里假设0。
        image_id = len(images)
        images.append({
            "file_name": file_name,
            "height": height,
            "id": image_id,
            "width": width
            
        })

        # 解析该图像下的box
        for box in image_node.findall('box'):
            left = int(box.attrib.get('left'))
            top = int(box.attrib.get('top'))
            w = int(box.attrib.get('width'))
            h = int(box.attrib.get('height'))

            # 解析label
            label_node = box.find('label')
            if label_node is not None:
                label_name = label_node.text.strip()
            else:
                label_name = "unknown"

            # 维护类别映射，给每个类别一个唯一id
            if label_name not in category_name_to_id:
                category_name_to_id[label_name] = category_id_counter
                categories.append({
                    "id": category_id_counter,
                    "name": label_name,
                    "supercategory": ""
                })
                category_id_counter += 1

            category_id = category_name_to_id[label_name]

            # 计算bbox和area
            bbox = [left, top, w, h]
            area = w * h

            annotations.append({
                "area": area,
                "bbox": bbox,
                "category_id": category_id,
                "id": annotation_id,
                "image_id": image_id,
                "iscrowd": 0
            })
            annotation_id += 1

    # 构建 info 字段（可以自定义）
    info = {
        "contributor": "",
        "date_created": "",
        "description": "Converted from XML",
        "url": "",
        "version": "1.0",
        "year": 2025
    }

    coco_dict = {
        "annotations": annotations,
        "categories": categories,
        "images": images,
        "info": info
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(coco_dict, f, ensure_ascii=False, indent=2)

    print(f"已生成 COCO 格式文件：{output_file}")


# 示例调用
convert_xml_to_coco(
    '/home2/item/jinlong/XMDK/git/gangkou_005_xiangmendakai/create_xmdk_det/create_xmdk_det/train.xml',  # 你的 XML 文件路径
    '/home2/item/jinlong/XMDK/git/gangkou_005_xiangmendakai/create_xmdk_det/create_xmdk_det/train.json',  # 输出 COCO JSON 路径
    '/home2/item/jinlong/XMDK/git/gangkou_005_xiangmendakai/create_xmdk_det/create_xmdk_det/images/train'
)

# # 示例调用
# convert_xml_to_coco(
#     xml_file='/home2/item/jinlong/XMDK/git/gangkou_005_xiangmendakai/create_xmdk_det/create_xmdk_det/test.xml.xml',
#     output_json='/home2/item/jinlong/XMDK/git/gangkou_005_xiangmendakai/create_xmdk_det/create_xmdk_det/test.xml.json'
# )
