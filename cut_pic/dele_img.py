#删除所有不是1080*1280的图片
import os
from PIL import Image
def delete_non_1080x1280_images(folder_path):
    """
    删除指定文件夹中所有不是1080x1280分辨率的图片。
    
    :param folder_path: 包含图片的文件夹路径
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif')):
            try:
                with Image.open(file_path) as img:
                    if img.size != (1080, 1280):
                        os.remove(file_path)
                        print(f"Deleted non-1080x1280 image: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
if __name__ == "__main__":
    folder_path = r"/home2/item/jinlong/DCFZ/git/ALLdata1/images/test_cropped"
    delete_non_1080x1280_images(folder_path)

    print("所有非1080x1280的图片已删除。")