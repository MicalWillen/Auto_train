import os
import matplotlib.pyplot as plt
import shutil
from tqdm import tqdm
from matplotlib.font_manager import FontProperties

# 统计数据集的各类缺陷次数
def count_defects_in_files(root_folder):
    """
    统计并返回指定目录下每个txt文件中缺陷类型的出现次数，并检查是否存在同名图片。
    """
    defect_counts = {}

    for filename in os.listdir(root_folder):
        if filename.endswith(".txt"):
            txt_name = os.path.splitext(filename)[0]
            file_path = os.path.join(root_folder, filename)
            image_exists = False

            # 检查是否存在同名的图片文件
            for ext in ('.jpg', '.bmp', '.jpeg'):
                image_path = os.path.join(root_folder, txt_name + ext)
                if os.path.exists(image_path):
                    image_exists = True
                    break

            try:
                with open(file_path, "r") as f:
                    for line in f:
                        try:
                            defect_type = int(line.split()[0])
                            if defect_type not in defect_counts:
                                defect_counts[defect_type] = 0
                            defect_counts[defect_type] += 1
                        except ValueError:
                            continue
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return defect_counts
# 将数据集依据缺陷类型移动文件到对应缺陷目录子文件夹中。
def move_files_by_defect_type(fileroot, picked_root, defect_types):
    """
    根据指定的缺陷类型范围，将源文件夹中的图片和标注文件移动到目标文件夹下的对应子文件夹中。
    如果没有找到图片，仍然会移动 .txt 文件。
    """
    os.makedirs(picked_root, exist_ok=True)

    filenames = [file for file in os.listdir(fileroot) if file.endswith(".txt")]

    for txtfile in tqdm(filenames):
        txt_path = os.path.join(fileroot, txtfile)
        base_name = txtfile[:-4]  # 去掉 .txt 扩展名

        # 尝试寻找不同扩展名的图片文件
        img_extensions = ('.jpg', '.bmp', '.png')
        img_path = None
        for ext in img_extensions:
            potential_img_path = os.path.join(fileroot, base_name + ext)
            if os.path.exists(potential_img_path):
                img_path = potential_img_path
                break

        matched_types = set()
        try:
            with open(txt_path, "r") as f:
                for line in f:
                    defect_type = int(line.split(" ")[0])
                    if defect_type in defect_types:
                        matched_types.add(defect_type)
        except Exception as e:
            print(f"Error reading {txtfile}: {e}")
            continue

        for defect_type in matched_types:
            defect_folder = os.path.join(picked_root, f"type_{defect_type}")
            os.makedirs(defect_folder, exist_ok=True)

            try:
                # 移动图片文件（如果有）
                if img_path is not None:
                    shutil.copy(img_path, os.path.join(defect_folder, os.path.basename(img_path)))

                # 总是移动 .txt 文件
                shutil.copy(txt_path, os.path.join(defect_folder, os.path.basename(txt_path)))
            except Exception as e:
                print(f"Error moving files for {txtfile} to {defect_folder}: {e}")

    print("所有文件均已处理并相应移动")

# 转换并排序缺陷类型合适的制图字典
def sort_dict_by_key_number(input_dict):
    """
    对字典按照键中的数字进行排序，并在新字典中去除'type_'前缀。
    """
    sorted_items = sorted(input_dict.items(), key=lambda item: int(item[0].split('_')[1]))
    sorted_dict = {item[0].split('_')[1]: item[1] for item in sorted_items}
    return sorted_dict
# 制作两个统计图：1.缺陷图像统计图 2.缺陷次数统计图
def plot_txt_counts_and_bar_chart(root_dir, root_folder):
    """
    统计指定目录下每个文件夹中的.txt文件数量，并绘制带有顶部标签的柱状图保存到指定路径。
    """
    classes_file_path = os.path.join(root_folder, 'classes.txt')
    if os.path.exists(classes_file_path):
        os.remove(classes_file_path)
        print(f"Deleted: {classes_file_path}")

    folder_txt_counts = {}
    output_file = os.path.join(root_dir, 'chart_with_labels.png')

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # 获取每个缺陷类型的出现次数
    defect_counts = count_defects_in_files(root_folder)

    # 转换并排序缺陷类型
    sorted_defect_counts = sort_dict_by_key_number({f'type_{key}': value for key, value in defect_counts.items()})
    print("1.缺陷图像统计图：")
    print(sorted_defect_counts)

    # 提取x轴和y轴数据
    x_defect = list(sorted_defect_counts.keys())
    y_defect = list(sorted_defect_counts.values())

    if x_defect and y_defect:
        bars_defect = ax[0].bar(x_defect, y_defect)

        # 设置字体加粗
        font_prop = FontProperties(weight='bold', size='large')

        # 在柱顶显示数量
        for bar in bars_defect:
            yval = bar.get_height()
            ax[0].text(bar.get_x() + bar.get_width() / 2, yval, str(yval), ha='center', va='bottom', fontsize=12,
                       fontproperties=font_prop)

        # 添加标题和坐标轴标签
        ax[0].set_title('数据集中各缺陷类型的出现次数', fontproperties=font_prop)
        ax[0].set_xlabel('缺陷类型', fontproperties=font_prop)
        ax[0].set_ylabel('出现次数', fontproperties=font_prop)

        # 设置x轴刻度标签
        ax[0].set_xticks(x_defect)
        ax[0].set_xticklabels(x_defect, fontproperties=font_prop)
    else:
        print("No defects were counted.")

    move_files_by_defect_type(root_folder, root_dir, defect_counts.keys())

    # 遍历根目录下的所有文件夹
    for foldername in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, foldername)
        if os.path.isdir(folder_path):
            txt_count = sum(1 for _ in os.listdir(folder_path) if _.endswith('.txt'))
            folder_txt_counts[foldername] = txt_count

    # 按照缺陷类型调整字典键名并排序
    sorted_folder_txt_counts = sort_dict_by_key_number(folder_txt_counts)
    print("2.缺陷次数统计图字典：")
    print(sorted_folder_txt_counts)

    # 提取x轴和y轴数据
    x = list(sorted_folder_txt_counts.keys())
    y = list(sorted_folder_txt_counts.values())

    # 设置字体
    plt.rcParams['font.family'] = 'Times New Roman, SimSun'
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 支持中文

    # 第一个图表：文件夹中的.txt文件数量
    bars = ax[1].bar(x, y, color='green')

    # 在柱顶显示数量
    for bar in bars:
        yval = bar.get_height()
        ax[1].text(bar.get_x() + bar.get_width() / 2, yval, str(yval), ha='center', va='bottom', fontsize=12,
                   fontproperties=font_prop)

    # 添加标题和坐标轴标签
    ax[1].set_title('数据集各对应缺陷出现图片数量', fontproperties=font_prop)
    ax[1].set_xlabel('缺陷类型', fontproperties=font_prop)
    ax[1].set_ylabel('图片数量', fontproperties=font_prop)

    # 设置x轴刻度标签
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(x, fontproperties=font_prop)

    # 确保保存图表的目录存在
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    # 保存图表文件
    plt.tight_layout()
    plt.savefig(output_file)

    # 显示图形
    # plt.show()

    print(f"图表已保存到: {output_file}")

# 示例调用
root_folder = r'/home2/item/jinlong/DCFZ/进模型/0603'
root_directory = os.path.join(root_folder,"picture") 

plot_txt_counts_and_bar_chart(root_directory, root_folder)



