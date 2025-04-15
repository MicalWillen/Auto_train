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

# 使用示例
apply_mask(r'D:\Document\desktop\1\test\108_0_0.bmp', r'D:\Document\desktop\1\test\108_0_0.json', 'output.png')
