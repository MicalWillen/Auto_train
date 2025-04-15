import csv
import os
import pandas as pd
from PyQt5.QtWidgets import QMessageBox, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class FormatOperationer:
    def __init__(self):
        # 初始化清空的数据变量
        self.send_msg = ""
        self.pdca_name = []
        self.data_output = []
        self.dynamic_list_file_exists = False
        self.dynamic_list = []

    def clear_send_msg(self):
        """ 清空 send_msg """
        self.send_msg = ""

    def clear_pdca_name(self):
        """ 清空 pdca_name """
        self.pdca_name = []

    def clear_data_output(self):
        """ 清空 data_output """
        self.data_output = []
    """ 用于处理 CSV 文件并填充到 QTableView """

    def read_para_csv(self, recipe_full_path):
        """ 读取 CSV 文件的标题行并返回列表 """
        try:
            if not recipe_full_path:
                return []

            df = pd.read_csv(recipe_full_path, encoding="utf-8")
            return list(df.columns)  # 返回标题行
        except Exception as e:
            QMessageBox.critical(None, "Initialization", f"Fail to read the data file!\n{e}")
            return []

    def fill_table_view(self, table_view: QTableView, data):
        """ 将数据填充到 QTableView """
        try:
            if not data or len(data) < 2:
                QMessageBox.warning(None, "Warning", "Invalid data structure!")
                return

            # 计算最大行数，保证所有数据都能填充
            max_rows = max(len(col) for col in data)

            # 创建 QStandardItemModel，列数为 data 的数组数
            num_cols = len(data)
            model = QStandardItemModel(max_rows, num_cols)

            # 设置表头
            headers = ["RAW name", "PDCA name"] + [f"PDCA name_{i}" for i in range(1, num_cols - 1)]
            model.setHorizontalHeaderLabels(headers)

            # 遍历行
            for row in range(max_rows):
                for col in range(num_cols):
                    value = ""
                    if row < len(data[col]):  # 确保不超出索引范围
                        value = str(data[col][row])  # 转换为字符串
                    model.setItem(row, col, QStandardItem(value))

            # 设置数据模型
            table_view.setModel(model)

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Fail to fill the data!\n{e}")

    def load_format_from_local(self, table_view):
        """ 加载本地 CSV 文件数据 """
        self.dynamic_list.clear()
        load_path = os.path.join(os.getcwd(), "Reflection_format.csv")
        if os.path.exists(load_path):
            self.dynamic_list_file_exists = True
            with open(load_path, "r", encoding="GBK") as f:
                reader = csv.reader(f)
                self.dynamic_list = [row for row in reader]
        else:
            self.dynamic_list_file_exists = False
            load_path = os.path.join(os.getcwd(), "DataFormat.csv")
            self.EQ_output_format = self.read_para_csv(load_path)

        if self.dynamic_list_file_exists:
            self.fill_table_view(table_view, self.dynamic_list)
        else:
            self.fill_table_view(table_view, self.EQ_output_format)
    def fill_table_view_multi_column(self, table_view: QTableView, data, real_time=False):
        """ 处理多列数据并填充到 QTableView """
        try:
            num_rows = len(data[0]) if data else 0
            num_cols = len(data)
            model = QStandardItemModel(num_rows, num_cols)

            for i in range(num_cols):
                header = f"PDCA {i+1}" if real_time else f"RAW Name {i+1}"
                model.setHorizontalHeaderItem(i, QStandardItem(header))

            for col_idx, col_data in enumerate(data):
                for row_idx, value in enumerate(col_data):
                    model.setItem(row_idx, col_idx, QStandardItem(value))

            table_view.setModel(model)  # 绑定数据模型
        except Exception as e:
            QMessageBox.critical(None, "Initialization", f"Fail to fill the data!\n{e}")

    def ReflectionDataSheet(self, data_outputs, dt):
        """ 映射数据表格，将数据输出为键值对格式 """
        # send_msg = ""
        # pdca_name = []
        # data_output = []

        for i in range(1, len(dt)):
            for j in range(len(dt[0])):
                if dt[i][j] and dt[i][j] != "-":
                    pn = dt[i][j]
                    data = data_outputs[i - 1][j]
                    self.send_msg += f"{pn}:{data},"
                    self.pdca_name.append(pn)
                    self.data_output.append(data)

        return self.send_msg, self.pdca_name, self.data_output

    def ReadOutputData(self, start_line, end_line, file_full_path):
        """ 读取输出数据，解析指定行范围的数据 """
        try:
            data_outputs = []
            with open(file_full_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            for j in range(start_line - 1, end_line + 1, 2):
                if j >= len(lines) - 1:
                    break
                line_cg = lines[j].strip().split(",")
                if len(line_cg[0]) < 10 or "[" in line_cg[0]:
                    continue
                line_bg = lines[j + 1].strip().split(",")

                data_outputs.append(line_cg)
                data_outputs.append(line_bg)

            return data_outputs
        except Exception as e:
            QMessageBox.critical(None, "Initialization", f"Fail to read the data file!\n{e}")
            return []
