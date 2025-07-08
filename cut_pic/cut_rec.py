import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def crop_and_save_images(input_image_folder, input_label_folder, output_image_folder, output_label_folder, top_left, bottom_right):
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_label_folder, exist_ok=True)

    for filename in os.listdir(input_image_folder):
        if not filename.lower().endswith(".jpg"):
            continue

        image_path = os.path.join(input_image_folder, filename)
        label_path = os.path.join(input_label_folder, filename.replace(".jpg", ".txt"))
        output_image_path = os.path.join(output_image_folder, filename)
        output_label_path = os.path.join(output_label_folder, filename.replace(".jpg", ".txt"))

        with Image.open(image_path) as img:
            width, height = img.size
            cropped_img = img.crop((*top_left, *bottom_right))
            cropped_width, cropped_height = cropped_img.size
            cropped_img.save(output_image_path)

        if not os.path.exists(label_path):
            # 空标签也生成空txt文件
            open(output_label_path, 'w').close()
            continue

        new_labels = []
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                class_id, cx, cy, w, h = parts
                cx = float(cx) * width
                cy = float(cy) * height
                w = float(w) * width
                h = float(h) * height

                x1 = cx - w / 2
                y1 = cy - h / 2
                x2 = cx + w / 2
                y2 = cy + h / 2

                crop_x1, crop_y1 = top_left
                crop_x2, crop_y2 = bottom_right

                # 检查是否和裁剪区域有交集
                if x2 <= crop_x1 or x1 >= crop_x2 or y2 <= crop_y1 or y1 >= crop_y2:
                    continue  # 完全在外部，跳过

                # 将边界框裁剪到crop区域内
                x1_clipped = max(x1, crop_x1)
                y1_clipped = max(y1, crop_y1)
                x2_clipped = min(x2, crop_x2)
                y2_clipped = min(y2, crop_y2)

                new_cx = (x1_clipped + x2_clipped) / 2 - crop_x1
                new_cy = (y1_clipped + y2_clipped) / 2 - crop_y1
                new_w = x2_clipped - x1_clipped
                new_h = y2_clipped - y1_clipped

                # 归一化
                new_cx /= cropped_width
                new_cy /= cropped_height
                new_w /= cropped_width
                new_h /= cropped_height

                # 限制在 [0, 1] 范围内
                new_cx = min(max(new_cx, 0), 1)
                new_cy = min(max(new_cy, 0), 1)
                new_w = min(max(new_w, 0), 1)
                new_h = min(max(new_h, 0), 1)

                new_labels.append(f"{class_id} {new_cx:.6f} {new_cy:.6f} {new_w:.6f} {new_h:.6f}")

        with open(output_label_path, 'w') as out_f:
            out_f.write("\n".join(new_labels) + ("\n" if new_labels else ""))

if __name__ == "__main__":
    input_image_folder = r"/home2/datsests/MOT/MOT20/train/train/1"
    input_label_folder = r"/home2/datsests/MOT/MOT20/train/train/1"
    output_image_folder = r"/home2/datsests/MOT/MOT20/train/train/13"
    output_label_folder = r"/home2/datsests/MOT/MOT20/train/train/13"

    top_left = (348, 0)
    bottom_right = (1628, 1080)
    crop_and_save_images(input_image_folder, input_label_folder, output_image_folder, output_label_folder, top_left, bottom_right)
