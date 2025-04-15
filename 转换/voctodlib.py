import os
import xml.etree.ElementTree as ET
from xml.dom import minidom  # 用于格式化 XML

def convert_annotations_to_dataset(image_folder, annotation_folder, output_file):
    # 创建新的 dataset 根节点
    dataset = ET.Element('dataset')
    name = ET.SubElement(dataset, 'name')
    comment = ET.SubElement(dataset, 'comment')
    images = ET.SubElement(dataset, 'images')

    # 遍历 annotation 文件夹中的所有 XML 文件
    for annotation_file in os.listdir(annotation_folder):
        if annotation_file.endswith('.xml'):
            annotation_path = os.path.join(annotation_folder, annotation_file)

            # 解析 XML 文件
            tree = ET.parse(annotation_path)
            root = tree.getroot()

            # 提取文件路径信息
            folder = root.find('folder').text
            filename = root.find('filename').text
            # 将绝对路径改为相对路径
            image_path = os.path.join(os.path.basename(image_folder), filename)

            # 创建 image 元素
            image = ET.SubElement(images, 'image', file=image_path)

            has_box = False  # 标记是否有标签
            for obj in root.findall('object'):
                bndbox = obj.find('bndbox')
                if bndbox is not None:
                    xmin = int(bndbox.find('xmin').text)
                    ymin = int(bndbox.find('ymin').text)
                    xmax = int(bndbox.find('xmax').text)
                    ymax = int(bndbox.find('ymax').text)

                    width = xmax - xmin
                    height = ymax - ymin

                    box = ET.SubElement(image, 'box', top=str(ymin), left=str(xmin), width=str(width), height=str(height))

                    label = ET.SubElement(box, 'label')
                    label.text = obj.find('name').text

                    has_box = True  # 存在标签

                    polygon = obj.find('polygon')
                    if polygon is not None:
                        i = 1
                        while True:
                            x = polygon.find(f'x{i}')
                            y = polygon.find(f'y{i}')
                            if x is None or y is None:
                                break
                            # 将 x 和 y 转换为整数后再写入属性
                            ET.SubElement(box, 'point', x=str(int(float(x.text))), y=str(int(float(y.text))))
                            i += 1

            # 如果没有标签，移除空的 image 元素
            # if not has_box:
            #     images.remove(image)

    # 将结果写入输出文件
    rough_string = ET.tostring(dataset, encoding='utf-8', method='xml')  # 修改为 utf-8
    reparsed = minidom.parseString(rough_string)
    with open(output_file, 'w', encoding='utf-8') as f:  # 修改为 utf-8
        f.write(reparsed.toprettyxml(indent="  "))

# 使用示例
convert_annotations_to_dataset(
    '/home/ps/AB/item/bentian/打刻/进模型/0331/xml/img',  # 图片路径文件夹
    '/home/ps/AB/item/bentian/打刻/进模型/0331/xml/Annotations',  # XML 标签文件夹
    '/home/ps/AB/item/bentian/打刻/进模型/0331/xml/img.xml'  # 输出文件
)