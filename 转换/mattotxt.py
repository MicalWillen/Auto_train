import os
from scipy.io import loadmat

def convert_mat_folder_to_yolo_txt(mat_folder, output_folder, img_width=640, img_height=360, class_id=0):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(mat_folder):
        if filename.endswith(".mat"):
            mat_path = os.path.join(mat_folder, filename)
            data = loadmat(mat_path)

            if 'loc' not in data:
                print(f"跳过 {filename}：未找到 'loc' 字段。")
                continue

            loc_data = data['loc']
            if loc_data.shape[1] != 2:
                print(f"跳过 {filename}：'loc' 字段不是 Nx2 格式。")
                continue

            # 归一化多边形点
            normalized_points = []
            for x, y in loc_data:
                normalized_points.append(x / img_width)
                normalized_points.append(y / img_height)

            # 生成 YOLO 格式行
            yolo_line = f"{class_id} " + " ".join(f"{pt:.6f}" for pt in normalized_points)

            # 保存 .txt 文件
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.txt")
            with open(output_path, 'w') as f:
                f.write(yolo_line + "\n")

    print("✅ 批量转换完成！")

# 使用示例
convert_mat_folder_to_yolo_txt(r"/home2/datsests/Beijing-BRT-dataset-master/train/111", r"/home2/datsests/Beijing-BRT-dataset-master/train/1111")
