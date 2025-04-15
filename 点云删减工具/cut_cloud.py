def delete_lines_by_interval(file_path, x, output_file=None):
    """
    按指定间隔删除文本文件中的行。
    
    :param file_path: 输入的文本文件路径
    :param x: 间隔，例如 x=3 表示每隔 3 行删除一行
    :param output_file: 输出的文件路径（如果为空，则覆盖原文件）
    """
    if x <= 0:
        print("间隔 x 必须为正整数！")
        return
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 按间隔删除行
        updated_lines = [line for i, line in enumerate(lines) if (i + 1) % x != 0]

        # 写入到输出文件
        if output_file is None:
            output_file = file_path  # 覆盖原文件
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)

        print(f"处理完成！已保存到 {output_file}")
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在！")
    except Exception as e:
        print(f"发生错误：{e}")

# 示例用法
file_path = r"D:\Document\文档\WeChat Files\wxid_0vbr78mjmrr522\FileStorage\File\2024-11\3DPointCloud\right.txt"  # 输入文件路径
x = 2  # 每隔3行删除一次
output_file = r"D:\Document\文档\WeChat Files\wxid_0vbr78mjmrr522\FileStorage\File\2024-11\3DPointCloud\1\right.txt"  # 输出文件路径（可以设置为 None 覆盖原文件）
delete_lines_by_interval(file_path, x, output_file)
delete_lines_by_interval(output_file, x, output_file)
