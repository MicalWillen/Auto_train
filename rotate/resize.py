import cv2
import numpy as np
import os

# 缩放图像和YOLO标签
def resize_image_and_labels(img, lines, scale_factor):
    org_height, org_width = img.shape[:2]

    # 计算缩放后的宽度和高度
    new_width = int(org_width * np.sqrt(scale_factor))
    new_height = int(org_height * np.sqrt(scale_factor))

    # 使用cv2.resize进行等比例缩放图像
    resized_image = cv2.resize(img, (new_width, new_height))

    resized_labels = []

    # 遍历每一行YOLO标签，调整它们的坐标和尺寸
    for line in lines:
        values = line.strip().split()
        if len(values) == 5:
            class_label, x_center, y_center, width, height = map(float, values)
            x_center *= new_width
            y_center *= new_height
            width *= new_width
            height *= new_height
            resized_labels.append([class_label, x_center, y_center, width, height])

    return resized_image, resized_labels


# 裁剪图像：裁剪出一个与原图大小一样的矩形区域
def crop_image(image, rect, img_width, img_height):
    x, y, w, h = rect
    x_min = int(x * img_width)
    y_min = int(y * img_height)
    x_max = int((x + w) * img_width)
    y_max = int((y + h) * img_height)

    x_min = max(0, x_min)
    y_min = max(0, y_min)
    x_max = min(img_width, x_max)
    y_max = min(img_height, y_max)

    if x_min >= x_max or y_min >= y_max:
        return None

    cropped_image = image[y_min:y_max, x_min:x_max]
    return cropped_image


# 更新YOLO标签：将标签更新到裁剪后的区域
def update_yolo_labels(labels, rect, img_width, img_height):
    x, y, w, h = rect
    x_min = int(x * img_width)
    y_min = int(y * img_height)
    x_max = int((x + w) * img_width)
    y_max = int((y + h) * img_height)

    updated_labels = []
    for label in labels:
        class_label, x_center, y_center, width, height = label
        new_x_center = (x_center * img_width - x_min) / (x_max - x_min)
        new_y_center = (y_center * img_height - y_min) / (y_max - y_min)
        new_width = width * img_width / (x_max - x_min)
        new_height = height * img_height / (y_max - y_min)

        if 0 <= new_x_center <= 1 and 0 <= new_y_center <= 1 and new_width > 0 and new_height > 0:
            updated_labels.append([class_label, new_x_center, new_y_center, new_width, new_height])

    return updated_labels


# 贪心算法：选择最少的矩形来覆盖所有目标
def min_covering_rectangles(rectangles, img_width, img_height):
    rectangles.sort(key=lambda r: (r[2], r[3]))  # 按照矩形的宽度和高度排序

    selected_rectangles = []
    covered = [False] * len(rectangles)

    # 贪心算法
    for i, rect in enumerate(rectangles):
        if not covered[i]:
            selected_rectangles.append(rect)
            x_min, y_min, w, h = rect
            for j in range(len(rectangles)):
                if not covered[j]:
                    rect_j = rectangles[j]
                    rect_j_x_min, rect_j_y_min, rect_j_w, rect_j_h = rect_j
                    if rect_j_x_min >= x_min and rect_j_y_min >= y_min and rect_j_x_min + rect_j_w <= x_min + w and rect_j_y_min + rect_j_h <= y_min + h:
                        covered[j] = True

    return selected_rectangles


# 主函数：处理图片和YOLO标签
def process_image_and_labels(image_path, label_path, scale=1.5):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    with open(label_path, 'r') as file:
        lines = file.readlines()

    resized_image, resized_labels = resize_image_and_labels(image, lines, scale)
    img_height, img_width, _ = resized_image.shape

    rectangles = [(label[1] - label[3]/2, label[2] - label[4]/2, label[3], label[4]) for label in resized_labels]

    selected_rectangles = min_covering_rectangles(rectangles, img_width, img_height)

    cropped_images = []
    updated_labels = []

    for i, rect in enumerate(selected_rectangles):
        cropped_image = crop_image(resized_image, rect, img_width, img_height)

        if cropped_image is None:
            continue

        cropped_images.append(cropped_image)

        new_labels = update_yolo_labels(resized_labels, rect, img_width, img_height)
        updated_labels.append(new_labels)

    os.makedirs("output_images", exist_ok=True)
    os.makedirs("output_labels", exist_ok=True)

    for i, (cropped_image, new_labels) in enumerate(zip(cropped_images, updated_labels)):
        if cropped_image is not None:
            cv2.imwrite(f"output_images/cropped_{i}.jpg", cropped_image)

            with open(f"output_labels/cropped_{i}.txt", 'w') as file:
                for label in new_labels:
                    file.write(" ".join(map(str, label)) + "\n")

# 测试代码
if __name__ == "__main__":

    # Example usage
    image_path = r'D:\WB\2\1\2024-12-17-19-21-22-542_3_11_WGP45110C570000W470D.bmp'  # Path to your image
    label_path = r'D:\WB\2\1\1_5(15).txt'  # Path to your YOLO label file
    scale_factor = 1.5  # 缩放因子

    process_image_and_labels(image_path, label_path, scale_factor)


