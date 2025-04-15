import os
import math
import cv2

class YoloRotate:
    def __init__(self):
        pass

    def rotate_point(self, x1, y1, x0, y0, theta, clockwise=False):
        angle_rad = math.radians(theta)
        if clockwise:
            x2 = (x1 - x0) * math.cos(angle_rad) + (y1 - y0) * math.sin(angle_rad) + x0
            y2 = (y1 - y0) * math.cos(angle_rad) - (x1 - x0) * math.sin(angle_rad) + y0
        else:
            x2 = (x1 - x0) * math.cos(angle_rad) - (y1 - y0) * math.sin(angle_rad) + x0
            y2 = (y1 - y0) * math.cos(angle_rad) + (x1 - x0) * math.sin(angle_rad) + y0
        return x2, y2

    def yolo_to_four_points(self, img_width, img_height, x_center, y_center, width, height):
        """
        Convert YOLO bbox format to four corner points in pixel coordinates.
        """
        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height

        half_w = width / 2
        half_h = height / 2
        points = [
            (x_center - half_w, y_center - half_h),  # top-left
            (x_center + half_w, y_center - half_h),  # top-right
            (x_center + half_w, y_center + half_h),  # bottom-right
            (x_center - half_w, y_center + half_h),  # bottom-left
        ]
        return points

    def four_points_to_yolo_format(self, img_width, img_height, points):
        """
        Convert four corner points in pixel coordinates back to YOLO format.
        """
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        x_center = (max(x_coords) + min(x_coords)) / 2
        y_center = (max(y_coords) + min(y_coords)) / 2
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)

        return (
            x_center / img_width,
            y_center / img_height,
            width / img_width,
            height / img_height,
        )

    def rotate_image_and_labels(self, image_path, labels, theta):
        """
        Rotate image and adjust YOLO labels accordingly.
        """
        # Load image
        img = cv2.imread(image_path)
        img_height, img_width = img.shape[:2]

        # Calculate rotation matrix and rotate the image
        center = (img_width / 2, img_height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, -1*theta, 1.0)
        rotated_img = cv2.warpAffine(
            img, rotation_matrix, (img_width, img_height), flags=cv2.INTER_LINEAR
        )

        # Rotate labels
        rotated_labels = []
        for label in labels:
            class_id, x_center, y_center, width, height = label
            points = self.yolo_to_four_points(img_width, img_height, x_center, y_center, width, height)

            # Rotate each point
            rotated_points = [
                self.rotate_point(x, y, center[0], center[1], theta) for x, y in points
            ]

            # Convert rotated points back to YOLO format
            rotated_yolo = self.four_points_to_yolo_format(img_width, img_height, rotated_points)
            rotated_labels.append((class_id, *rotated_yolo))

        return rotated_img, rotated_labels


def process_folder_images_and_labels(input_img_folder, input_lbl_folder, output_img_folder, output_lbl_folder, theta):
    """
    Rotate all images and corresponding YOLO labels in a folder.
    """
    # Ensure output folders exist
    os.makedirs(output_img_folder, exist_ok=True)
    os.makedirs(output_lbl_folder, exist_ok=True)

    yolo_rotate = YoloRotate()

    for file_name in os.listdir(input_img_folder):
        if file_name.endswith(".bmp") or file_name.endswith(".png"):
            # File paths
            img_path = os.path.join(input_img_folder, file_name)
            lbl_path = os.path.join(input_lbl_folder, file_name.replace(".bmp", ".txt").replace(".png", ".txt"))
            output_img_path = os.path.join(output_img_folder, file_name)
            output_lbl_path = os.path.join(output_lbl_folder, file_name.replace(".bmp", ".txt").replace(".png", ".txt"))

            # Read labels
            labels = read_labels(lbl_path)

            # Rotate image and labels
            rotated_img, rotated_labels = yolo_rotate.rotate_image_and_labels(img_path, labels, theta)

            # Save rotated image
            cv2.imwrite(output_img_path, rotated_img)

            # Save rotated labels
            write_labels(output_lbl_path, rotated_labels)

            print(f"Processed: {img_path} -> {output_img_path}")


def read_labels(file_path):
    """
    Read YOLO label file with multiple encoding attempts.
    """
    if not file_path.endswith(".txt"):
        print(f"Skipping non-label file: {file_path}")
        return []
    
    encodings = ['utf-8', 'gbk', 'latin1', 'gb18030']
    
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding, errors='ignore') as f:
                labels = []
                for line in f.readlines():
                    parts = line.strip().split()
                    
                    # Ensure the line has the correct format (class_id and bbox coordinates)
                    if len(parts) != 5:
                        print(f"Skipping invalid label line in {file_path}: {line}")
                        continue
                    
                    try:
                        class_id = int(parts[0])  # Convert class ID to integer
                        bbox = tuple(map(float, parts[1:]))  # Convert bbox to float values
                        labels.append((class_id, *bbox))
                    except ValueError:
                        print(f"Skipping invalid data in {file_path}: {line}")
                        continue
                
                return labels
        except (UnicodeDecodeError, FileNotFoundError) as e:
            print(f"Failed to read {file_path} with encoding {encoding}: {e}")
            continue
    
    raise ValueError(f"Failed to decode file: {file_path}")


def write_labels(file_path, labels):
    """
    Write YOLO label file.
    """
    with open(file_path, "w") as f:
        for label in labels:
            line = f"{label[0]} {' '.join(map(str, label[1:]))}\n"
            f.write(line)


# 示例调用
input_img_folder = r"D:\WB\2\1"  # 输入图片文件夹路径
input_lbl_folder = input_img_folder # 输入标签文件夹路径
output_img_folder = r"D:\WB\3"  # 输出图片文件夹路径
output_lbl_folder = output_img_folder  # 输出标签文件夹路径
theta = 3  # 顺时针旋转1度

process_folder_images_and_labels(input_img_folder, input_lbl_folder, output_img_folder, output_lbl_folder, theta)
