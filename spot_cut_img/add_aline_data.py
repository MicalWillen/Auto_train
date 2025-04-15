import os

def append_line_to_txt_files(folder_path, line_to_add):
    """
    为指定文件夹中的所有 .txt 文件添加一行数据，并避免额外的空行。

    Args:
        folder_path (str): 文件夹路径。
        line_to_add (str): 要添加的行内容。
    """
    if not os.path.isdir(folder_path):
        print(f"错误: {folder_path} 不是有效的文件夹路径。")
        return

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # 仅处理 .txt 文件
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            try:
                with open(file_path, 'rb+') as file:  # 打开文件并确保二进制模式读写
                    file.seek(0, os.SEEK_END)  # 定位到文件末尾
                    if file.tell() > 0:  # 文件不为空时检查最后一个字符
                        file.seek(-1, os.SEEK_END)
                        last_char = file.read(1)
                        if last_char != b'\n':  # 如果最后一个字符不是换行符
                            file.write(b'\n')  # 添加换行符
                    file.write((line_to_add + '\n').encode('utf-8'))
                print(f"已成功添加数据到 {file_name}")
            except Exception as e:
                print(f"添加数据到 {file_name} 失败: {e}")


folder_path = r"D:\FR\每日存\241202\1202新标注\反面"  # 替换为你的文件夹路径
line_to_add = r"0 0.728752 0.172501 0.067502 0.069999"  # 替换为你想添加的行内容
append_line_to_txt_files(folder_path, line_to_add)
