import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableView, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class FormatOperation:
    """ 处理 CSV 文件并填充到 QTableView """

    def read_para_csv(self, file_path): # 读取 CSV 文件并返回列表
        """ 读取 CSV 文件的前三行并返回列表 """
        try:
            if not file_path or not os.path.exists(file_path):
                return []

            df = pd.read_csv(file_path, header=None,encoding="GBK")

            # 处理 CSV 的列名、第一行和第二行数据
            csv_data = [
                list(df.iloc[0]) if len(df) > 0 else [],  # 标题行
                list(df.iloc[1]) if len(df) > 0 else [],  # 第一行
                list(df.iloc[2]) if len(df) > 1 else []   # 第二行
            ]
            return csv_data
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Fail to read the data file!\n{e}")
            return []

    def fill_table_view(self, table_view: QTableView, data):
        """ 将数据填充到 QTableView """
        try:
            if not data or len(data) < 3:
                QMessageBox.warning(None, "Warning", "Invalid data structure!")
                return

            # 计算最大行数，保证所有数据都能填充
            max_rows = max(len(data[0]), len(data[1]), len(data[2]))

            # 创建 QStandardItemModel，列数为 3
            model = QStandardItemModel(max_rows, 3)
            model.setHorizontalHeaderLabels(["RAW name", "PDCA name", "PDCA name_3"])

            # 遍历行
            for row in range(max_rows):
                for col in range(3):
                    value = ""
                    if row < len(data[col]):  # 确保不超出索引范围
                        value = str(data[col][row])  # 转换为字符串
                    model.setItem(row, col, QStandardItem(value))

            # 设置数据模型
            table_view.setModel(model)

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Fail to fill the data!\n{e}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.fo = FormatOperation()
        self.dynamic_list = []
        self.dynamic_list_file_exists = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PDCA Data Manager")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.btn_setup = QPushButton("Setup Data Format")
        self.btn_setup.clicked.connect(self.setup_format)

        self.btn_load = QPushButton("Load Data from Local")
        self.btn_load.clicked.connect(self.load_format_from_local)

        self.table_view = QTableView()

        self.layout.addWidget(self.btn_setup)
        self.layout.addWidget(self.btn_load)
        self.layout.addWidget(self.table_view)

        self.setLayout(self.layout)

    def setup_format(self):
        """ 选择 CSV 文件并加载数据格式 """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            headers = self.fo.read_para_csv(file_path)
            if headers:
                self.fo.fill_table_view(self.table_view, headers)
                self.dynamic_list = headers

    def load_format_from_local(self):
        """ 从本地加载 Reflection_format.csv """
        local_path = os.path.join(os.getcwd(), "Reflection_format.csv")
        if os.path.exists(local_path):
            self.dynamic_list_file_exists = True
            headers = self.fo.read_para_csv(local_path)
            if headers:
                self.fo.fill_table_view(self.table_view, headers)
                self.dynamic_list = headers
        else:
            QMessageBox.warning(self, "Warning", "Reflection_format.csv not found!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.load_format_from_local()
    window.show()
    sys.exit(app.exec_())
