import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import shutil


def crop_and_save_images(input_image_folder, input_label_folder, output_image_folder, output_label_folder, top_left,
                         bottom_right):
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)
    if not os.path.exists(output_label_folder):
        os.makedirs(output_label_folder)

    for filename in os.listdir(input_image_folder):
        if filename.endswith(".bmp"):
            image_path = os.path.join(input_image_folder, filename)
            label_path = os.path.join(input_label_folder, filename.replace(".bmp", ".txt"))

            # Load image
            with Image.open(image_path) as img:
                width, height = img.size
                cropped_img = img.crop((*top_left, *bottom_right))
                cropped_width, cropped_height = cropped_img.size

                # Save cropped image
                cropped_img.save(os.path.join(output_image_folder, filename))

                # Adjust label coordinates
                if os.path.exists(label_path):
                    with open(label_path, 'r') as label_file:
                        labels = label_file.readlines()

                    new_labels = []
                    for label in labels:
                        parts = label.strip().split()
                        if len(parts) == 5:
                            class_id, cx, cy, w, h = parts
                            cx = float(cx) * width
                            cy = float(cy) * height
                            w = float(w) * width
                            h = float(h) * height

                            # Check if the center of the box is within the crop area
                            if (top_left[0] <= cx <= bottom_right[0]) and (top_left[1] <= cy <= bottom_right[1]):
                                # Adjust coordinates for the cropped image
                                new_cx = (cx - top_left[0]) / cropped_width
                                new_cy = (cy - top_left[1]) / cropped_height
                                new_w = w / cropped_width
                                new_h = h / cropped_height

                                new_labels.append(f"{class_id} {new_cx:.6f} {new_cy:.6f} {new_w:.6f} {new_h:.6f}")

                    # Save new labels
                    new_label_path = os.path.join(output_label_folder, filename.replace(".bmp", ".txt"))
                    with open(new_label_path, 'w') as new_label_file:
                        new_label_file.write("\n".join(new_labels))


if __name__ == "__main__":
    input_image_folder = r"D:\国显\1\1"
    input_label_folder = r"D:\国显\1\1"
    output_image_folder = r"D:\国显\4\1"
    output_label_folder = r"D:\国显\4\1"

    # Define the top left and bottom right points of the cropping rectangle
    # top_left = (2384, 637)
    # bottom_right = (7596-2290, 7496-650)

    # top_left = (1308, 676)
    # bottom_right = (5188, 6243)

    top_left = (4080, 3390)
    bottom_right = (10304,7119)
    crop_and_save_images(input_image_folder, input_label_folder, output_image_folder, output_label_folder, top_left,
                         bottom_right)
