import math
import os
from PIL import Image

def aut_clu_lap(image_path,grid_size):
    with Image.open(image_path) as img:
        width, height = img.size
        width_numbers=width/grid_size
        width_numbers=math.ceil(width_numbers)
        width_result=int((width_numbers*grid_size-width)/(width_numbers-1))

        height_numbers=height/grid_size
        height_numbers=math.ceil(height_numbers)
        height_result=int((height_numbers*grid_size-height)/(height_numbers-1))


    return width_result,height_result
def crop_to_grid(input_image_folder, input_label_folder, output_image_folder, output_label_folder, grid_size=1024):
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
                width_lap,height_lap=aut_clu_lap(image_path,grid_size)
                # Calculate step size (taking overlap into account)
                width_step_size = grid_size - width_lap
                height_step_size= grid_size - height_lap
                # Iterate over image grid
                for i in range(0, width-width_step_size, width_step_size):
                    for j in range(0, height-height_step_size, height_step_size):
                        # Define the cropping area
                        left = i
                        top = j
                        right = i + grid_size
                        bottom = j + grid_size

                        # Crop the image
                        cropped_img = img.crop((left, top, right, bottom))
                        cropped_width, cropped_height = cropped_img.size

                        # Generate new filename with suffix
                        suffix = f"_x{i}_y{j}"
                        cropped_filename = filename.replace(".bmp", f"{suffix}.bmp")
                        cropped_img.save(os.path.join(output_image_folder, cropped_filename))

                        # Adjust and save labels for the cropped image
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

                                    # Check if the center of the bounding box is within the current crop
                                    if (left <= cx <= right) and (top <= cy <= bottom):
                                        # Adjust the bounding box for the cropped image
                                        new_cx = (cx - left) / cropped_width
                                        new_cy = (cy - top) / cropped_height
                                        new_w = w / cropped_width
                                        new_h = h / cropped_height

                                        new_labels.append(
                                            f"{class_id} {new_cx:.6f} {new_cy:.6f} {new_w:.6f} {new_h:.6f}")

                            # Save new labels
                            new_label_filename = filename.replace(".bmp", f"{suffix}.txt")
                            new_label_path = os.path.join(output_label_folder, new_label_filename)
                            with open(new_label_path, 'w') as new_label_file:
                                new_label_file.write("\n".join(new_labels))


if __name__ == "__main__":
    input_image_folder = r"D:\国显\4\2类图\2_black"
    input_label_folder = input_image_folder
    output_image_folder = r"D:\国显\4\cut\2_black_cut"
    output_label_folder = output_image_folder

    grid_size = 2048  # Size of the grid for cropping
    # overlap =aut_clu_lap(grid_size)  # Overlap between crops
    
    # grid_size = 840  # Size of the grid for cropping
    # overlap =34  # Overlap between crops

    crop_to_grid(input_image_folder, input_label_folder, output_image_folder, output_label_folder, grid_size)
# from PIL import Image
# import os

# def crop_image(image_path, output_folder, crop_size=2048, overlap=0):
#     """
#     将大图裁剪成小图并保存。
#     :param image_path: 原始图片路径
#     :param output_folder: 裁剪后小图保存路径
#     :param crop_size: 裁剪区域大小（默认2048*2048）
#     :param overlap: 裁剪区域的重叠大小（默认0）
#     """
#     # 打开图片
#     image = Image.open(image_path)
#     width, height = image.size

#     # 创建保存文件夹
#     os.makedirs(output_folder, exist_ok=True)

#     # 计算裁剪步长
#     step = crop_size - overlap

#     # 开始裁剪
#     count = 0
#     for top in range(0, height - crop_size + 1, step):
#         for left in range(0, width - crop_size + 1, step):
#             box = (left, top, left + crop_size, top + crop_size)
#             cropped_image = image.crop(box)
#             cropped_image.save(os.path.join(output_folder, f"crop_{count}.png"))
#             count += 1

#     print(f"裁剪完成！共生成 {count} 张图片。")

# # 示例使用
# image_path = r"D:\国显\4\test\33BH291QC03-161325_F_64gray.bmp"  # 替换为你的图片路径
# output_folder = r"D:\国显\4\cut\1"  # 替换为输出文件夹路径
# crop_image(image_path, output_folder, crop_size=2048, overlap=256)
