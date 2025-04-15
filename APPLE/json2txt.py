import json
import os
import glob
import os.path as osp

def get_class_list(jsonfileList):
    """
    获取所有json文件中的类别集合
    :param jsonfileList: JSON文件列表
    :return: classList：类别集合
    """
    class_set = set()
    for jsonfile in jsonfileList:
        with open(jsonfile, "r") as f:
            file_in = json.load(f)
            shapes = file_in["shapes"]
            for shape in shapes:
                class_set.add(shape["label"])  # 添加类别标签到集合中
    return list(class_set)

def labelme2yolo(jsonfilePath="", resultDirPath="", classList=None):
    """
    此函数将labelme软件标注好的数据集转换为YOLO格式的数据集
    :param jsonfilePath: labelme标注好的*.json文件所在文件夹
    :param resultDirPath: 转换好后的*.txt保存文件夹
    :param classList: 数据集中的类别标签（如果未提供，将自动获取）
    :return:
    """
    # 0.创建保存转换结果的文件夹
    if not os.path.exists(resultDirPath):
        os.mkdir(resultDirPath)

    # 1.获取目录下所有的labelme标注好的Json文件，存入列表中
    jsonfileList = glob.glob(osp.join(jsonfilePath, "*.json"))
    print(jsonfileList)  # 打印文件夹下的文件名称

    # 2.如果没有提供classList，自动从JSON文件中提取
    if classList is None:
        classList = get_class_list(jsonfileList)
        print(f"自动获取的类别集合: {classList}")

    # 3.遍历json文件，进行转换
    for jsonfile in jsonfileList:
        # 4. 打开json文件
        with open(jsonfile, "r") as f:
            file_in = json.load(f)
            shapes = file_in["shapes"]

            # 5. 使用图像名称创建一个txt文件，用来保存数据
            with open(osp.join(resultDirPath, osp.basename(jsonfile).replace(".json", ".txt")), "w") as file_handle:
                for shape in shapes:
                    class_id = classList.index(shape["label"])  # 根据类别标签获取类别ID

                    # 6. 获取轮廓中的所有点，计算边界框的坐标
                    x_points = [point[0] for point in shape["points"]]
                    y_points = [point[1] for point in shape["points"]]

                    x_min = min(x_points)
                    y_min = min(y_points)
                    x_max = max(x_points)
                    y_max = max(y_points)

                    # 7. 计算中心点坐标和宽高
                    x_center = (x_min + x_max) / 2.0 / file_in["imageWidth"]
                    y_center = (y_min + y_max) / 2.0 / file_in["imageHeight"]
                    width = (x_max - x_min) / file_in["imageWidth"]
                    height = (y_max - y_min) / file_in["imageHeight"]

                    # 8. 将结果写入txt文件
                    file_handle.writelines(f"{class_id} {x_center} {y_center} {width} {height}\n")

if __name__ == "__main__":
    jsonfilePath = r"D:\Document\desktop\22222\image\train"  # 要转换的json文件所在目录
    resultDirPath = r"D:\Document\desktop\22222\image\1"  # 要生成的txt文件夹
    # classList=['AY-QX-S4', 'BD-QX-S4', 'BH-QX-S4', 'BX-QX-S4', 'CJ-QX-S4', 'CNCDX-QX-S4', 'CNCGQ-QX-S4', 'DLM-QX-S4', 'DL-QX-S4', 'DMH-QX-S4', 'DW-QX-S4', 'GB-QX-S4', 'GM-QX-S4', 'GY-QX-S4', 'HS-QX-S4', 'HX-QX-S4', 'LBKDK-QX-S4', 'LBKMB-QX-S4', 'LBKYW-QX-S4', 'LDD-QX-S4', 'LD-QX-S4', 'LH-QX-S4', 'LKYW-QX-S4', 'LVX-QX-S4', 'LX-QX-S4', 'LY-QX-S4', 'MB-QX-S4', 'MD-QX-S4', 'MSJB-QX-S4', 'PHCXR-QX-S4', 'PHL3KJ-QX-S4', 'PH-QX-S4', 'PMPS-QX-S4', 'PMPW-QX-S4', 'PMQQ-QX-S4', 'PMQS-QX-S4', 'PMZZ-QX-S4', 'PS-QX-S4', 'TB-QX-S4', 'TJ-QX-S4', 'YH-QX-S4', 'YIS-QX-S4', 'YS-QX-S4', 'YW-QX-S4', 'ZKYS-QX-S4', 'ZW-QX-S4', 'ignoer-QX-S4', 'ignore-KBJ-S1', 'ignore-QX-S1', 'igonre-QX-S4']
    
    labelme2yolo(jsonfilePath=jsonfilePath, resultDirPath=resultDirPath,classList=None)
