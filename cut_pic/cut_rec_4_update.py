import os
import cv2
import numpy as np


# 用于裁剪和调整YOLO标签
def crop_and_adjust_label(image, crop_x_min, crop_y_min, crop_size, label):
    img_height, img_width = image.shape[:2]
    class_id, x_center, y_center, width, height = label

    # 计算中心点在原图像的实际坐标
    x_center_abs = x_center * img_width
    y_center_abs = y_center * img_height

    # 检查是否在给定矩形范围内
    if (given_x_min <= x_center_abs <= given_x_max) and (given_y_min <= y_center_abs <= given_y_max):
        return None  # 如果在矩形内则排除

    # 调整标签位置到裁剪后的区域
    x_center_new = (x_center_abs - crop_x_min) / crop_size
    y_center_new = (y_center_abs - crop_y_min) / crop_size
    width_new = width * img_width / crop_size
    height_new = height * img_height / crop_size

    # 检查是否在裁剪区域内
    if not (0 <= x_center_new <= 1 and 0 <= y_center_new <= 1):
        return None  # 如果不在裁剪区域内则排除

    return [class_id, x_center_new, y_center_new, width_new, height_new]


# 裁剪矩形边框附近的512x512区域
def crop_along_bbox(image, bbox, crop_size=800, step=800):
    img_height, img_width = image.shape[:2]
    x_min, y_min, x_max, y_max = bbox
    crops = []

    # 从矩形框四边开始裁剪
    for x in range(x_min, x_max, step):
        crop_x_min = max(0, x - crop_size // 2)
        crop_y_min = max(0, y_min - crop_size // 2)
        crop_x_max = min(img_width, crop_x_min + crop_size)
        crop_y_max = min(img_height, crop_y_min + crop_size)
        crops.append((crop_x_min, crop_y_min, crop_x_max, crop_y_max))

        crop_y_min = max(0, y_max - crop_size // 2)
        crop_y_max = min(img_height, crop_y_min + crop_size)
        crops.append((crop_x_min, crop_y_min, crop_x_max, crop_y_max))

    for y in range(y_min, y_max, step):
        crop_x_min = max(0, x_min - crop_size // 2)
        crop_y_min = max(0, y - crop_size // 2)
        crop_x_max = min(img_width, crop_x_min + crop_size)
        crop_y_max = min(img_height, crop_y_min + crop_size)
        crops.append((crop_x_min, crop_y_min, crop_x_max, crop_y_max))

        crop_x_min = max(0, x_max - crop_size // 2)
        crop_x_max = min(img_width, crop_x_min + crop_size)
        crops.append((crop_x_min, crop_y_min, crop_x_max, crop_y_max))

    return crops


# 处理文件夹
def process_folder(image_folder, label_folder, output_image_folder, output_label_folder, bbox, crop_size=800):
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)
    if not os.path.exists(output_label_folder):
        os.makedirs(output_label_folder)

    image_files = [f for f in os.listdir(image_folder) if f.endswith('.bmp')]
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        label_path = os.path.join(label_folder, image_file.replace('.bmp', '.txt'))

        # 读取图像和标签
        image = cv2.imread(image_path)
        with open(label_path, 'r') as f:
            labels = [list(map(float, line.strip().split())) for line in f]

        # 获取沿矩形框裁剪的多个512x512区域
        crop_coords = crop_along_bbox(image, bbox, crop_size=crop_size)
        for idx, (crop_x_min, crop_y_min, crop_x_max, crop_y_max) in enumerate(crop_coords):
            cropped_img = image[crop_y_min:crop_y_max, crop_x_min:crop_x_max]
            output_labels = []

            # 处理每个标签并调整到新的裁剪区域
            for label in labels:
                new_label = crop_and_adjust_label(image, crop_x_min, crop_y_min, crop_size, label)
                if new_label is not None:
                    output_labels.append(new_label)

                # 保存裁剪后的图像
                output_image_path = os.path.join(output_image_folder, f'{image_file.replace(".bmp", "")}_crop_{idx}.bmp')
                cv2.imwrite(output_image_path, cropped_img)

            # 如果有有效标签则保存裁剪后的图像和标签
            if output_labels:
                output_image_path = os.path.join(output_image_folder,
                                                 f'{image_file.replace(".bmp", "")}_crop_{idx}.bmp')
                # cv2.imwrite(output_image_path, cropped_img) #这里暂时不保存图片

                output_label_path = os.path.join(output_label_folder,
                                                 f'{image_file.replace(".bmp", "")}_crop_{idx}.txt')
                with open(output_label_path, 'w') as f:
                    for label in output_labels:
                        f.write(f"{int(label[0])} {label[1]:.6f} {label[2]:.6f} {label[3]:.6f} {label[4]:.6f}\n")


# 示例用法
if __name__ == "__main__":
    image_folder = r"D:\xinwu_yolo\yolov50628\yolo0910-org\785-ALL\youmoqu\15-2_3\c3"
    label_folder = r"D:\xinwu_yolo\yolov50628\yolo0910-org\labels"
    output_image_folder = r"D:\xinwu_yolo\yolov50628\yolo0910-org\785-ALL\youmoqu\15-2_3\15-2_3_ink"
    output_label_folder = r"D:\xinwu_yolo\yolov50628\yolo0910-org\785-ALL\youmoqu\15-2_3\15-2_3_labels"

    # 给定矩形框的左上角和右下角 (x_min, y_min, x_max, y_max)
    # bbox = (2384-200, 637-190, 7596 - 2290 + 15+100, 7496 - 650 + 15 + 15+90+30)  # 根据实际情况修改
    bbox = (590, 0, 5006, 4912)  # 根据实际情况修改
    given_x_min, given_y_min, given_x_max, given_y_max = bbox

    # 开始处理
    process_folder(image_folder, label_folder, output_image_folder, output_label_folder, bbox)
