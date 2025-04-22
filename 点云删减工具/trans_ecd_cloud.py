import struct
import os

class HeightData:
    def __init__(self, width, height, x_interval, y_interval, z_interval, data):
        self.width = width
        self.height = height
        self.x_interval = x_interval
        self.y_interval = y_interval
        self.z_interval = z_interval
        self.data = data

def read_ecd_to_point_cloud(ecd_file, output_txt):
    try:
        with open(ecd_file, 'rb') as f:
            # 读取文件头
            version = struct.unpack('I', f.read(4))[0]
            width = struct.unpack('i', f.read(4))[0]
            height = struct.unpack('i', f.read(4))[0]
            x_interval = struct.unpack('d', f.read(8))[0]
            y_interval = struct.unpack('d', f.read(8))[0]
            reserve_u = struct.unpack('i', f.read(4))[0]

            # 跳过文件头剩余部分
            f.seek(10240, 0)

            # 读取高度数据
            data_len = width * height
            data = struct.unpack(f'{data_len}i', f.read(data_len * 4))

            # 创建 HeightData 对象
            height_data = HeightData(
                width=width,
                height=height,
                x_interval=x_interval,
                y_interval=y_interval,
                z_interval=0.00001,  # zInterval 固定为 0.00001 mm
                data=data
            )

            # 将数据转换为点云格式
            with open(output_txt, 'w') as out:
                for row in range(height_data.height):
                    for col in range(height_data.width):
                        z = height_data.data[row * height_data.width + col]
                        if z != -1000000000:  # 跳过无效值
                            x = col * height_data.x_interval
                            y = row * height_data.y_interval
                            z = z * height_data.z_interval  # 转换为 mm
                            out.write(f"{x:.4f} {y:.4f} {z:.4f}\n")  # 限制小数点后4位
        print(f"转换完成：{ecd_file} -> {output_txt}")
    except Exception as e:
        print(f"处理文件 {ecd_file} 时发生错误: {e}")

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.ecd'):
                ecd_file_path = os.path.join(root, file)
                output_txt_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.txt")
                read_ecd_to_point_cloud(ecd_file_path, output_txt_path)

# 示例调用
input_folder = r"D:\Defult\Desktop\202502101\DL6MA23250210C0215\OP3D扫描1"  # 替换为包含 .ecd 文件的文件夹路径
output_folder = r"D:\Defult\Desktop\202502101\output"  # 替换为输出文件夹路径
process_folder(input_folder, output_folder)