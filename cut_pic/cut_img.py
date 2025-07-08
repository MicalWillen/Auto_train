import os
import cv2
from concurrent.futures import ThreadPoolExecutor

def crop_image_only(image_path, output_image_folder, crop_region):
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Failed to load: {image_path}")
        return

    crop_x1, crop_y1, crop_x2, crop_y2 = crop_region
    crop = image[crop_y1:crop_y2, crop_x1:crop_x2]

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_image_path = os.path.join(output_image_folder, f"{base_name}.jpg")
    # 保存为JPEG，设置质量参数为95（可调范围：0-100）
    cv2.imwrite(output_image_path, crop, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"[OK] Saved: {output_image_path}")

def process_image_folder_multithread(image_folder, output_image_folder, crop_region, num_threads=8):
    os.makedirs(output_image_folder, exist_ok=True)
    supported_exts = (".png", ".jpg", ".jpeg", ".bmp")

    image_files = [
        file for file in os.listdir(image_folder)   
        if file.lower().endswith(supported_exts)
    ]

    def task(file):
        image_path = os.path.join(image_folder, file)
        crop_image_only(image_path, output_image_folder, crop_region)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(task, image_files)

if __name__ == "__main__":
    image_folder = r"/home2/item/jinlong/DCFZ-cut/每日存/0703/250630/frames/1-1"
    output_image_folder = r"/home2/item/jinlong/DCFZ-cut/每日存/0703/250630/frames/1-1_cropped"
    crop_region = (0, 640, 1080, 1920)  # (x1, y1, x2, y2)
    # crop_region = (790, 343, 1302, 855)  # (x1, y1, x2, y2)
    process_image_folder_multithread(
        image_folder,
        output_image_folder,
        crop_region,
        num_threads=12  # 根据CPU核数调整
    )
