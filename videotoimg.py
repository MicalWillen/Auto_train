import cv2
import os

def video_to_images(video_folder, output_folder):
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取视频文件名并排序
    videos = [vid for vid in os.listdir(video_folder) if vid.endswith((".mp4", ".avi", ".mov"))]
    videos.sort()  # 确保顺序正确

    if not videos:
        print("没有找到视频文件")
        return

    global_frame_count = 0  # 全局帧计数器

    for video in videos:
        video_path = os.path.join(video_folder, video)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"无法打开视频: {video_path}")
            continue

        # 为当前视频创建单独的输出文件夹
        video_output_folder = os.path.join(output_folder, os.path.splitext(video)[0])
        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 保存帧到当前视频的输出文件夹，文件名包含视频名和全局帧编号
            frame_filename = f"{os.path.splitext(video)[0]}_frame_{global_frame_count:06d}.jpg"
            frame_path = os.path.join(video_output_folder, frame_filename)
            cv2.imwrite(frame_path, frame)
            global_frame_count += 1

        cap.release()
        print(f"视频 {video} 的帧已保存到 {video_output_folder}")

# 示例用法
video_to_images("/home2/item/jinlong/DCFZ-cut/每日存/0703/250630/71-大车防撞-2025-06-30", "/home2/item/jinlong/DCFZ-cut/每日存/0703/250630/frames")