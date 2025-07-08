import os
import json
from tqdm import tqdm
from PIL import Image

def convert_yolo_to_coco(txt_folder, image_folder, output_file, class_names):
    """
    将 YOLO 格式的目标检测数据转换为 COCO 格式。
    
    :param txt_folder: YOLO txt 文件所在文件夹路径
    :param image_folder: 图像文件所在文件夹路径
    :param output_file: 输出的 COCO JSON 文件路径
    :param class_names: 类别名称列表，按 YOLO 格式中的类别索引顺序排列
    """
    images = []
    annotations = []
    categories = []
    annotation_id = 0

    # 创建类别映射
    for idx, class_name in enumerate(class_names):
        categories.append({
            "id": idx,
            "name": class_name,
            "supercategory": ""
        })

    # 遍历图片文件夹
    for image_file in tqdm(os.listdir(image_folder)):
        if not image_file.lower().endswith(('jpg', 'jpeg', 'png')):
            continue

        image_path = os.path.join(image_folder, image_file)
        txt_file = os.path.join(txt_folder, os.path.splitext(image_file)[0] + '.txt')

        if not os.path.exists(txt_file):
            print(f"警告: 未找到图像 {image_file} 对应的标注文件 {txt_file}")
            continue

        # 获取图像宽高
        with Image.open(image_path) as img:
            width, height = img.size

        image_id = len(images)
        images.append({
            "file_name": image_file,
            "height": height,
            "id": image_id,
            "width": width
        })

        # 解析 YOLO txt 文件
        with open(txt_file, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"警告: 文件 {txt_file} 中存在格式错误的行: {line}")
                    continue

                class_id, x_center, y_center, box_width, box_height = map(float, parts)
                class_id = int(class_id)

                # 转换为 COCO 格式的 bbox
                left = (x_center - box_width / 2) * width
                top = (y_center - box_height / 2) * height
                w = box_width * width
                h = box_height * height

                annotations.append({
                    "area": w * h,
                    "bbox": [left, top, w, h],
                    "category_id": class_id,
                    "id": annotation_id,
                    "image_id": image_id,
                    "iscrowd": 0
                })
                annotation_id += 1

    # 构建 info 字段（可以自定义）
    info = {
        "contributor": "",
        "date_created": "",
        "description": "Converted from YOLO",
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


def get_class_names_from_txt(txt_folder):
    """
    从 YOLO txt 文件中提取所有标签并生成类别名称列表。
    
    :param txt_folder: YOLO txt 文件所在文件夹路径
    :return: 类别名称列表
    """
    class_names = set()
    for txt_file in os.listdir(txt_folder):
        if txt_file.endswith('.txt'):
            with open(os.path.join(txt_folder, txt_file), 'r') as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id = int(parts[0])
                        class_names.add(class_id)
    # 按类别 ID 排序
    return [str(class_id) for class_id in sorted(class_names)]


# 动态生成 class_names
txt_folder = '/home2/item/RFDETR/jiaqi_seg/test/images/yolov5_img_train/labels'  # YOLO txt 文件路径
class_names = get_class_names_from_txt(txt_folder)

# 示例调用
convert_yolo_to_coco(
    txt_folder=txt_folder,  # YOLO txt 文件路径
    image_folder='/home2/item/RFDETR/jiaqi_seg/test/images/yolov5_img_train/images',  # 图像文件路径
    output_file='/home2/item/RFDETR/jiaqi_seg/test/images/yolov5_img_train/images.json',  # 输出 COCO JSON 文件路径
    class_names=class_names  # 动态生成的类别名称列表
)