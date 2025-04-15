import os

def remove_last_line_from_txt_files(folder_path):

    if not os.path.isdir(folder_path):
        print(f"错误: {folder_path} 不是有效的文件夹路径。")
        return


    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

     
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            try:
                with open(file_path, 'r+', encoding='utf-8') as file:  
                    lines = file.readlines() 
                    if lines and lines[-1].strip() == "":  
                        file.seek(0)  
                        file.writelines(lines[:-1])  
                        file.truncate()  
                        print(f"已成功删除 {file_name} 的最后一行")
                    else:
                        print(f"跳过 {file_name}，最后一行不是换行符")
            except Exception as e:
                print(f"删除 {file_name} 的最后一行失败: {e}")

folder_path = r"D:\FR\每日存\241213\front\labeled"  
remove_last_line_from_txt_files(folder_path)
