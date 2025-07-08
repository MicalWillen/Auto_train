import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

def rotate_and_save(input_path, output_path, angle):
    try:
        with Image.open(input_path) as img:
            rotated_img = img.rotate(angle, expand=True)
            rotated_img.save(output_path)
            print(f"已旋转并保存: {output_path}")
    except Exception as e:
        print(f"处理文件 {input_path} 时出错: {e}")

def rotate_images_in_folder(input_folder, output_folder, angle, max_workers=24):
    """
    多线程旋转文件夹中的所有图片并保存到另一个文件夹。
    
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param angle: 旋转角度（顺时针）
    :param max_workers: 最大线程数
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for filename in os.listdir(input_folder):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                tasks.append(executor.submit(rotate_and_save, input_path, output_path, angle))
        
        # 可选：等待所有任务完成
        for future in as_completed(tasks):
            future.result()

if __name__ == "__main__":
    filedir=r"/home2/item/jinlong/DCFZ-cut/每日存/0703/250630/frames"
    input_folder = os.path.join(filedir, "1")
    output_folder = os.path.join(filedir, "1-1")
    angle = 90
    rotate_images_in_folder(input_folder, output_folder, float(angle))
    input_folder = os.path.join(filedir, "2")
    output_folder = os.path.join(filedir, "2-1")
    angle = -90
    rotate_images_in_folder(input_folder, output_folder, float(angle))
    # input_folder = os.path.join(filedir, "3")
    # output_folder = os.path.join(filedir, "3-1")
    # angle = -90
    # rotate_images_in_folder(input_folder, output_folder, float(angle))
    # input_folder = os.path.join(filedir, "4")       
    # output_folder = os.path.join(filedir, "4-1")
    # angle = 90
    # rotate_images_in_folder(input_folder, output_folder, float(angle))

    print("所有图片已处理完成。")
