import os
from PIL import Image
from tqdm import tqdm


def crop_images_by_labels(image_dir, label_dir,output_dir):
    # 确保输出目录存在
  
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取所有标签文件
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

    # 遍历标签文件夹中的所有标签文件
    for label_file in tqdm(label_files, desc='Processing labels', unit='file'):
        # 获取图片文件名
        image_file = label_file.replace('.txt', '.bmp')
        if image_file in os.listdir(image_dir):
            # 读取图片
            image_path = os.path.join(image_dir, image_file)
            image = Image.open(image_path)
            image_width, image_height = image.size

            # 读取标签文件
            with open(os.path.join(label_dir, label_file), 'r') as f:
                lines = f.readlines()
            lines = [line.strip() for line in lines]
            
            # 遍历标签中的每个目标，添加计数器
            for i, line in enumerate(tqdm(lines, desc=f'Cropping {label_file}', unit='object')):
                class_index, x_center, y_center, width, height = map(float, line.split())
                class_index = int(class_index)
                if class_index==100:
                    # 计算边界框的实际坐标
                    x_min = (x_center - width / 2) * image_width
                    y_min = (y_center - height / 2) * image_height
                    x_max = (x_center + width / 2) * image_width
                    y_max = (y_center + height / 2) * image_height

                    # 确保坐标在图片范围内
                    x_min, y_min, x_max, y_max = map(int, [max(0, min(x_min, image_width - 1)),
                                                        max(0, min(y_min, image_height - 1)),
                                                        max(0, min(x_max, image_width - 1)),
                                                        max(0, min(y_max, image_height - 1))])

                    # 裁剪图片
                    cropped_image = image.crop((x_min, y_min, x_max, y_max))
                    cropped_width, cropped_height = cropped_image.size
                    # 创建类别文件夹
                    class_dir = os.path.join(output_dir, str(class_index))
                    if not os.path.exists(class_dir):
                        os.makedirs(class_dir)
                    path_name=os.path.join(class_dir, f'{os.path.splitext(image_file)[0]}_{class_index}_{i}')
                    # 保存裁剪后的图片，文件名增加计数器 i
                    cropped_image.save(os.path.join(class_dir, f'{os.path.splitext(image_file)[0]}_{class_index}_{i}.bmp'))
                    print("save successfully")
                    new_labels = []
                    for i, line in enumerate(tqdm(lines, desc=f'Cropping {label_file}', unit='object')):
                        class_index, x_center, y_center, width, height = map(float, line.split())
                        class_index = int(class_index)
                        left =x_min
                        top  =y_min
                        right =x_max
                        bottom=y_max
                        
                        if class_index!=100:
                            x_center = float(x_center) * image_width
                            y_center = float(y_center) * image_height
                            width = float(width) * image_width
                            height = float(height) * image_height

                            # Check if the center of the bounding box is within the current crop
                            if (left <= x_center <= right) and (top <= y_center <= bottom):
                                # Adjust the bounding box for the cropped image
                                new_cx = (x_center - left) / cropped_width
                                new_cy = (y_center - top) / cropped_height
                                new_w = width / cropped_width
                                new_h = height / cropped_height

                                new_labels.append(
                                    f"{class_index} {new_cx:.6f} {new_cy:.6f} {new_w:.6f} {new_h:.6f}")
                    new_label_path=path_name+'.txt'
                    with open(new_label_path, 'w') as new_label_file:
                            new_label_file.write("\n".join(new_labels))

                            





# 使用示例
image_dir = r'D:\FR\每日存\241202\1202新标注\堵孔'
output_dir = r'D:\FR\每日存\241202\1202新标注\1111'
label_dir = image_dir
crop_images_by_labels(image_dir, label_dir,output_dir)
