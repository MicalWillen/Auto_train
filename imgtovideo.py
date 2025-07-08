import cv2
import os

def images_to_video(image_folder, output_video, fps=30):
    # 获取图片文件名并排序
    images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".png"))]
    images.sort()  # 确保顺序正确

    if not images:
        print("没有找到图片文件")
        return

    # 读取第一张图获取尺寸
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # 定义视频编码器和输出文件
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 可改为 'XVID', 'MJPG' 等
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        if frame is None:
            print(f"无法读取图片: {img_path}")
            continue
        video.write(frame)

    video.release()
    print(f"视频保存到: {output_video}")

# 示例用法
images_to_video("/home/ps/AB/framework/rf-detr-develop/pridect/26 /output_images", "/home/ps/AB/framework/rf-detr-develop/pridect/26 /output_images_cropped.mp4", fps=30)
