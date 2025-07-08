import os
import json
import cv2
import numpy as np
from PIL import Image

def apply_mask(image_path, json_path, output_path):
    # 读取图片
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    # 创建一个白色背景
    mask = np.ones((height, width), dtype=np.uint8) * 0
    
    # 读取JSON标注文件
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # 提取多边形坐标，并将多边形区域涂黑
    for shape in data['shapes']:
        if shape['shape_type'] == 'polygon':
            points = np.array(shape['points'], dtype=np.int32)
            cv2.fillPoly(mask, [points], 255)  # 将多边形区域涂黑
    
    # 保存结果
    result_image = Image.fromarray(mask)
    result_image.save(output_path)

def process_folder(image_folder, json_folder, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍历图片文件夹中的所有文件
    for image_file in os.listdir(image_folder):
        if image_file.endswith('.bmp') or image_file.endswith('.jpg') or image_file.endswith('.png'):
            # 构建对应的 JSON 文件路径
            json_file = os.path.splitext(image_file)[0] + '.json'
            image_path = os.path.join(image_folder, image_file)
            json_path = os.path.join(json_folder, json_file)
            output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + '_mask.png')
            
            # 检查 JSON 文件是否存在
            if os.path.exists(json_path):
                apply_mask(image_path, json_path, output_path)
                print(f"Processed: {image_file}")
            else:
                print(f"JSON file not found for: {image_file}")

# 使用示例
process_folder(
    r'/home2/item/FX/cotracker/0630/111/PutBox1',  # 图片文件夹路径
    r'/home2/item/FX/cotracker/0630/111/PutBox1',   # JSON 文件夹路径
    r'/home2/item/FX/cotracker/0630/111/PutBox11'  # 输出文件夹路径
)