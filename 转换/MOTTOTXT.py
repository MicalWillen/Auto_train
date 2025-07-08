import os

def mot_to_yolo_labels(mot_txt_path, output_dir, img_width=1920, img_height=1080):
    os.makedirs(output_dir, exist_ok=True)

    with open(mot_txt_path, 'r') as f:
        lines = f.readlines()

    frame_dict = {}

    for line in lines:
        fields = line.strip().split(',')
        if len(fields) < 9:
            continue  # 跳过格式不完整的行

        frame_id = int(fields[0])
        obj_id = int(fields[1])
        x = float(fields[2])
        y = float(fields[3])
        w = float(fields[4])
        h = float(fields[5])
        conf = float(fields[6])
        cls_id = int(fields[7])
        vis = float(fields[8])

        # 转换为 YOLO 格式（归一化后的中心点+宽高）
        x_center = (x + w / 2) / img_width
        y_center = (y + h / 2) / img_height
        w_norm = w / img_width
        h_norm = h / img_height

        yolo_line = f"{cls_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}"

        # 加入对应帧的标签
        frame_key = f"{frame_id:06d}.txt"
        frame_dict.setdefault(frame_key, []).append(yolo_line)

    # 写入每帧的标签文件
    for fname, yolo_lines in frame_dict.items():
        with open(os.path.join(output_dir, fname), 'w') as out_f:
            out_f.write('\n'.join(yolo_lines) + '\n')

    print(f"转换完成，共生成 {len(frame_dict)} 个 YOLO 标签文件，保存在：{output_dir}")

# 示例用法
if __name__ == "__main__":
    mot_txt_path = r"/home2/datsests/MOT/MOT20/train/MOT20-05/gt/gt.txt"      # 输入的MOT标签路径
    output_dir = "/home2/datsests/MOT/MOT20/train/MOT20-05/yolo"           # 输出目录
    img_width = 1654
    img_height = 1080

    mot_to_yolo_labels(mot_txt_path, output_dir, img_width, img_height)
