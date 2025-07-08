import os
from tqdm import tqdm

def remove_extra_files(root_dir, valid_extensions=[".jpg", ".bmp",".png"], check_extension=".txt"):
    """
    删除没有对应txt文件的jpg或bmp文件。

    参数:
    root_dir (str): 文件所在的目录
    valid_extensions (list): 需要检查的图像文件后缀名列表
    check_extension (str): 作为对比依据的文件后缀名
    """
    jpg_namelist = []
    txt_namelist = []

    # 遍历目录下的所有文件
    for filename in tqdm(os.listdir(root_dir)):
        file_stem, file_extension = os.path.splitext(filename)
        if file_extension in valid_extensions:  # 检查是否为图像文件
            jpg_namelist.append(file_stem)
        if file_extension == check_extension:   # 检查是否为txt文件
            txt_namelist.append(file_stem)

    # 检查是否存在图像文件
    if len(jpg_namelist) == 0:
        raise Exception(f"No files with extensions {valid_extensions} found.")

    # 删除没有对应txt文件的图像文件
    for jpg_filename in jpg_namelist:
        if jpg_filename not in txt_namelist:
            for ext in valid_extensions:
                file_path = os.path.join(root_dir, jpg_filename + ext)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Removed: {file_path}")

if __name__ == "__main__":
    root = r"/home/ps/AB/framework/rf-detr-develop/pridect/22/output_images"
    remove_extra_files(root)
