import os
import glob
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageEnhance



def process_images(file1, file2, file3, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 打开图像并转换为灰度
    img3 = Image.open(file1).convert("L")
    img2 = Image.open(file2).convert("L")
    img1 = Image.open(file3).convert("L")

    img1 = img1.resize((98, 99))
    img2 = img2.resize((98, 99))
    img3 = img3.resize((98, 99))

    # 合并图像成 RGB
    img = Image.merge("RGB", (img1, img2, img3))

    # 提取文件名
    name1 = os.path.splitext(os.path.basename(file1))[0]
    name2 = os.path.splitext(os.path.basename(file2))[0]
    name3 = os.path.splitext(os.path.basename(file3))[0]

    # 构造输出文件路径
    output_file = os.path.join(output_folder, f"{name1}_{name2}_{name3}.png")

    
    img.save(output_file)
    # 调用保存标签函数
    save_label(file1, file2, file3, output_folder, name1, name2, name3)

def save_label(file1, file2, file3, output_folder, name1, name2, name3):
    """
    合并三个文件的标签，按 'label, x, y, w, h' 格式保存，标签文件与图像文件名一致。
    """
    try:
        labels = []
        for file in [file1, file2, file3]:
            label_file = os.path.splitext(file)[0] + ".txt"  # 假设标签文件与图像文件同名
            if os.path.exists(label_file):
                with open(label_file, "r") as f:
                    lines = f.readlines()
                    labels.extend(lines)  # 读取所有标签

        # 如果有有效标签，保存到输出文件
        if labels:
            output_label_file = os.path.join(output_folder, f"{name1}_{name2}_{name3}.txt")
            with open(output_label_file, "a") as f:
                for label in labels:
                    f.write(label)  # 保留原始格式
            print(f"Saved labels for {file1}, {file2}, {file3}")
        else:
            print(f"No labels found for {file1}, {file2}, {file3}")

    except Exception as e:
        print(f"Error saving labels for {file1}, {file2}, {file3}: {e}")
def remove_light(string, light):
    name = '_' + light
    return string.replace(name, '')

def process_folder(folder1, folder2, folder3, output_folder, max_threads=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 支持多种格式
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    files1 = []
    files2 = []
    files3 = []

    for ext in extensions:
        files1.extend(glob.glob(os.path.join(folder1, ext)))
        files2.extend(glob.glob(os.path.join(folder2, ext)))
        files3.extend(glob.glob(os.path.join(folder3, ext)))

    # 创建文件名映射字典
    file_dict_2 = {remove_light(os.path.basename(f), "L1"): f for f in files2}
    file_dict_3 = {remove_light(os.path.basename(f), "L2"): f for f in files3}

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        try:
            for file1 in tqdm(files1):
                prefix = remove_light(os.path.basename(file1), "L0")
                file2 = file_dict_2.get(prefix)
                file3 = file_dict_3.get(prefix)
                if file2 and file3:
                    futures.append(executor.submit(process_images, file1, file2, file3, output_folder))

            for future in futures:
                future.result()

        except KeyboardInterrupt:
            print("\n捕获到中断信号，正在停止所有线程...")
            executor.shutdown(wait=False)  # 尝试立即停止线程
            raise  # 重新抛出中断信号

def main():
    folder = r'D:\VGA\apple'
    folder0 = os.path.join(folder, 'L0')
    folder1 = os.path.join(folder, 'L1')
    folder2 = os.path.join(folder, 'L2')

    output_folder = os.path.join(folder, 'result6')

    # 控制最大并发线程数为 5
    process_folder(folder0, folder1, folder2, output_folder, max_threads=8)

#根据名称遍历融合
# def main():
#     folder = r'D:\国显\原图图片'
#     output_folder = r"D:\国显\2"
#     images = ["F_64gray", "F_128gray", "F_black", "F_blue", "F_EVEN", "F_green", "F_red", "F_white"]

#     # 遍历所有子文件夹
#     for folder_name in tqdm(os.listdir(folder), desc="Processing Folders"):
#         current_folder = os.path.join(folder, folder_name)
#         outimage_folder = os.path.join(output_folder, folder_name)

#         # 三重循环生成所有组合
#         for i in tqdm(range(len(images)), desc=f"Processing Images in {folder_name}", leave=False):
#             for j in range(len(images)):
#                 with ThreadPoolExecutor(max_workers=8) as executor:
#                     futures = []
#                     try:
#                         for k in range(len(images)):
#                             # 检查是否有两个名称相同的图像
#                             if (i == j) or (j == k) or (i == k):
#                                 continue
                            
#                             # 构造文件路径
#                             file1 = os.path.join(current_folder, images[i] + ".bmp")
#                             file2 = os.path.join(current_folder, images[j] + ".bmp")
#                             file3 = os.path.join(current_folder, images[k] + ".bmp")
#                             label1 = os.path.join(current_folder, images[i] + ".txt")
#                             label2 = os.path.join(current_folder, images[j] + ".txt")
#                             label3 = os.path.join(current_folder, images[k] + ".txt")

#                             # 检查文件是否存在
#                             if os.path.exists(file1) and os.path.exists(file2) and os.path.exists(file3):
#                                 # 调用处理函数
#                                 # process_images(file1, file2, file3, outimage_folder)
#                                  futures.append(executor.submit(process_images, file1, file2, file3, outimage_folder))
                                
#                             else:
#                                 print(f"Skipping combination: {file1}, {file2}, {file3}. File not found!")
#                     except KeyboardInterrupt:
#                         print("\n捕获到中断信号，正在停止所有线程...")
#                         executor.shutdown(wait=False)  # 尝试立即停止线程
#                         raise  # 重新抛出中断信号

if __name__ == "__main__":
    main()
# import os
# from PIL import Image
# Image.MAX_IMAGE_PIXELS = None
# import torch
# from torchvision.transforms import ToTensor, ToPILImage

# # 将图像加载到 GPU
# def load_image_to_tensor(file_path, device="cuda"):
#     img = Image.open(file_path).convert("L")  # 转换为灰度
#     tensor = ToTensor()(img).to(device)  # [C, H, W]
#     return tensor

# # 在 GPU 上合并图像并保存
# def process_images(file1, file2, file3, output_folder, device="cuda"):
#     # 加载图像到 GPU
#     img1 = load_image_to_tensor(file1, device)
#     img2 = load_image_to_tensor(file2, device)
#     img3 = load_image_to_tensor(file3, device)

#     # 合并为 RGB 图像
#     merged_tensor = torch.stack((img1, img2, img3), dim=0).squeeze(1)  # [3, H, W]

#     # 转回 CPU 并转换为 PIL 图像
#     merged_image = ToPILImage()(merged_tensor.cpu())

#     # 构造输出文件路径
#     name1 = os.path.splitext(os.path.basename(file1))[0]
#     name2 = os.path.splitext(os.path.basename(file2))[0]
#     name3 = os.path.splitext(os.path.basename(file3))[0]
#     output_file = os.path.join(output_folder, f"{name1}_{name2}_{name3}.png")

#     # 保存图像
#     merged_image.save(output_file)
# # 主函数
# def main():
#     folder = r'D:\国显\原图图片\33BH291QC03-161325'
#     output_folder = r"D:\国显\1"
#     images = ["F_64gray", "F_128gray", "F_black", "F_blue", "F_EVEN", "F_green", "F_red", "F_white"]

#     # 确保输出文件夹存在
#     os.makedirs(output_folder, exist_ok=True)

#     # 使用 GPU 设备
#     device = "cuda" if torch.cuda.is_available() else "cpu"

#     # 三重循环生成所有组合
#     for i in range(len(images)):
#         for j in range(i + 1, len(images)):
#             for k in range(j + 1, len(images)):
#                 # 构造文件路径
#                 file1 = os.path.join(folder, images[i] + ".bmp")
#                 file2 = os.path.join(folder, images[j] + ".bmp")
#                 file3 = os.path.join(folder, images[k] + ".bmp")

#                 # 调用处理函数
#                 process_images(file1, file2, file3, output_folder, device)
# if __name__ == "__main__":
#     main()


