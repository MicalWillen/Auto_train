import os
from PIL import Image
import argparse
import random
from tqdm import tqdm

def rotate_image_multiple_times(input_path, output_folder, num_rotations, min_angle, max_angle):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开图像文件
    image = Image.open(input_path)

    # 获取文件名和扩展名
    filename, file_extension = os.path.splitext(os.path.basename(input_path))

    # 遍历每次旋转并保存
    for i in tqdm(range(num_rotations), desc='Processing rotations', unit='rotation'):
        # 生成随机角度
        rotation = random.uniform(min_angle, max_angle)

        rotated_image = image.rotate(rotation, resample=Image.BICUBIC)

        # 构造保存文件名，添加旋转角度的后缀
        # output_filename = f"{filename}_rotated_{i}_{int(rotation)}{file_extension}"
        output_filename = f"{filename}{file_extension}"
        output_path = os.path.join(output_folder, output_filename)

        # 保存旋转后的图像
        rotated_image.save(output_path)

def batch_rotate_images(input_folder, output_folder, num_rotations, min_angle, max_angle):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有图片文件
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 遍历每个图片文件并多次随机旋转保存
    for image_file in tqdm(image_files, desc='Processing images', unit='image'):
        input_path = os.path.join(input_folder, image_file)
        rotate_image_multiple_times(input_path, output_folder, num_rotations, min_angle, max_angle)

if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description='Batch rotate images in a folder with random angles.')
    parser.add_argument('--input_folder', default=r"F:\11111\guo", help='Path to the input image folder.')
    parser.add_argument('--output_folder', default=r"F:\11111\rotate3", help='Path to save the rotated images.')
    parser.add_argument('--num_rotations', type=int, default=1, help='Number of rotations to perform for each image. Default is 5.')
    parser.add_argument('--min_angle', type=float, default=3, help='Minimum rotation angle in degrees. Default is 30.')
    parser.add_argument('--max_angle', type=float, default=3, help='Maximum rotation angle in degrees. Default is 90.')

    args = parser.parse_args()

    # 调用函数进行图像批量旋转
    batch_rotate_images(args.input_folder, args.output_folder, args.num_rotations, args.min_angle, args.max_angle)

