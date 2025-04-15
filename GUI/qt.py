import csv
import os
import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout,
                             QVBoxLayout, QTableView, QHeaderView, QMainWindow, QAction,QMenu)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox)

from FormatOperation import FormatOperationer
import TriggerPDCA
from monitor import *


class GeneralSettingWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)  # 指定父窗口
        self.setWindowTitle("General Setting")
        self.parent_window = parent_window  # 记录主窗口，便于计算位置
        # 创建标签
        tcp_ip_label = QLabel("TCP/IP")
        directory_label = QLabel("Directory Path")

        # 创建文本框
        self.tcp_ip_edit = QLineEdit(parent_window.tcpip)
        self.port_edit = QLineEdit(parent_window.port)
        self.directory_edit = QLineEdit(parent_window.pathroot)
        # 获取参数值
        # if parent_window is not None:
        #     self.tcp_ip_edit.setText(parent_window.tcpip)
        #     self.port_edit.setText(parent_window.port)
        #     self.directory_edit.setText(parent_window.pathroot)

        # 创建按钮
        self.select_button = QPushButton("...")
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        # 设置布局
        # TCP/IP 和端口布局
        tcp_layout = QHBoxLayout()
        tcp_layout.addWidget(tcp_ip_label)
        tcp_layout.addWidget(self.tcp_ip_edit)
        port_label = QLabel("Port")
        tcp_layout.addWidget(port_label)
        tcp_layout.addWidget(self.port_edit)

        # 文件夹路径布局
        directory_layout = QHBoxLayout()
        directory_layout.addWidget(directory_label)
        directory_layout.addWidget(self.directory_edit)
        directory_layout.addWidget(self.select_button)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(tcp_layout)
        main_layout.addLayout(directory_layout)
        main_layout.addLayout(button_layout)

        # 创建中央部件并设置布局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 连接信号与槽
        self.select_button.clicked.connect(self.select_directory)
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.close)
        # 设置为模态窗口
        self.setWindowModality(Qt.WindowModal)
    def select_directory(self):
        # 弹出文件夹选择对话框
        directory = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if directory:
            self.directory_edit.setText(directory)
    def save_settings(self):
        # 在这里实现保存设置的功能
        # 你可以读取 self.tcp_ip_edit, self.port_edit 和 self.directory_edit 的值
        # 并将它们保存到文件或注册表中
        tcp_ip = self.tcp_ip_edit.text()
        port = self.port_edit.text()
        directory = self.directory_edit.text()

        # 保存到文件
        file_path = os.path.join(os.getcwd(), "systemsetup.txt")
        try:
            with open(file_path, "w", encoding="GBK") as f:
                f.write(f"{tcp_ip}\n")
                f.write(f"{port}\n")
                f.write(f"{directory}\n")
                QMessageBox.information(self, "Success", "Settings saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")
        # print("保存设置")
        self.close()
    def closeEvent(self, event):
        # 重新加载主页面的数据
        self.parent_window.load_system_setup()
        event.accept()
    

class SetupWindow(QMainWindow):
    """Setup 窗体，包含菜单栏和表格"""
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.setWindowTitle("General Setting")
        self.resize(800, 600)
        self.parent_window = parent_window  # 记录主窗口，便于计算位置
        self.dynamic_list = []
        # 计算位置，避免与主窗体重叠
        self.move_to_side()

        # 创建菜单栏
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("Operation")
        # settings_menu.aboutToShow.connect(self.open_general_setting)
        # 创建菜单项
        general_action = QAction("General Setting", self)
        general_action.triggered.connect(self.open_general_setting)
        settings_menu.addAction(general_action)
        
        # 创建表格
        self.table_view = QTableView()
        # self.model = QStandardItemModel(len(data.T), 3)
        # self.model.setHorizontalHeaderLabels(["RAW name", "PDCA name", "PDCA name_3"])

        # 表头加粗
        font = QFont()
        font.setBold(True)
        self.table_view.horizontalHeader().setFont(font)

        # 启用表头排序
        self.table_view.setSortingEnabled(True)

        # 交替行颜色
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setStyleSheet("QTableView { alternate-background-color: #f0f0f0; }")

        # 让列宽自适应窗口大小
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 填充数据
        # data = data.T
        # for i in range(len(data)):
        #     for j in range(min(3, len(data.columns))):  # 确保不越界
        #         item = QStandardItem(str(data.iloc[i, j]))
        #         item.setEditable(False)
        #         self.model.setItem(i, j, item)

        # self.table_view.setModel(self.model)

        # 设置布局
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        FormatOperationer().load_format_from_local(self.table_view)
        # 设置为模态窗口
        self.setWindowModality(Qt.WindowModal)
    def move_to_side(self):
        """让窗口不会覆盖主窗口"""
        parent_geometry = self.parent_window.geometry()
        #+parent_geometry.width()
        new_x = parent_geometry.x()  + 20
        new_y = parent_geometry.y()
        self.move(new_x, new_y)

    def open_general_setting(self):
        """打开 General Setting 窗口"""
        self.general_setting_window = GeneralSettingWindow(self.parent_window)
        self.general_setting_window.setWindowModality(Qt.WindowModal)  # 设置为模态窗口
        self.general_setting_window.show()
        # self.general_setting_window.setFocus()
    def save_settings(self):
        # 在这里实现保存设置的功能
        # 你可以读取 self.tcp_ip_edit, self.port_edit 和 self.directory_edit 的值
        # 并将它们保存到文件或注册表中
        print("保存设置")
        self.close()
    def contextMenuEvent(self, event):
        """右键菜单"""
        menu = QMenu(self)

        addColumnAction = QAction("Add Column", self)
        addColumnAction.triggered.connect(self.add_column)
        menu.addAction(addColumnAction)

        saveFormatAction = QAction("Save Format", self)
        saveFormatAction.triggered.connect(self.save_format)
        menu.addAction(saveFormatAction)

        menu.exec_(self.mapToGlobal(event.pos()))  # 显示菜单
    def add_column(self):
        """添加新列，值为空"""
        column_count = self.table_view.model().columnCount()
        model = self.table_view.model()
        if model:
            model.setColumnCount(column_count + 1)
            for row in range(model.rowCount()):
                model.setItem(row, column_count, QStandardItem("-"))
        self.table_view.model().setHeaderData(column_count, Qt.Horizontal, f"PDCA name_{column_count - 1}")

    def save_format(self):
        """保存数据格式到 CSV"""
        reply = QMessageBox.question(self, "Information", "Do you want to save this format?",
                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # 默认选 No

        if reply == QMessageBox.Yes:
            self.dynamic_list.clear()
            for col in range(self.table_view.model().columnCount()):
                column_data = []
                for row in range(self.table_view.model().rowCount()):
                    item = self.table_view.model().item(row, col)
                    column_data.append(item.text() if item else "-")  # 避免空值
                self.dynamic_list.append(column_data)

            # 删除旧的 CSV 文件
            file_path = os.path.join(os.getcwd(), "Reflection_format.csv")
            if os.path.exists(file_path):
                os.remove(file_path)

            # 重新写入 CSV 文件
            with open(file_path, "w", newline="", encoding="GBK") as file:
                writer = csv.writer(file)
                writer.writerows(self.dynamic_list)  # 转置后写入 CSV
    #关闭窗口时触发
    def closeEvent(self, event):
        # self.parent_window.load_system_setup()
        #重新加载主页面的数据
        self.parent_window.fo.load_format_from_local(self.parent_window.table_view)
class DataWindow(QWidget):
    """主窗体，包含按钮和表格"""
    def __init__(self):
        super().__init__()
        # 初始化变量
        # self.dynamic_list = []
        # self.dynamic_list_file_exists = False
        
        self.fo = FormatOperationer()
        self.EQ_output_format = []
        # 读取CSV文件
        # csv_file = r"D:\Document\desktop\1\Reflection_format.csv"  # 替换成你的CSV文件路径
        # self.data = pd.read_csv(csv_file, header=None, encoding='GBK')
        self.load_system_setup()
        self.setWindowTitle("WCA BALI")
        self.resize(800, 600)  # 初始大小，可调整
        # self.tcpip = ""
        # self.port =""
        # self.pathroot=""
        # 创建表格
        self.table_view = QTableView()
        # self.model = QStandardItemModel(len(self.data.T), 3)
        # self.model.setHorizontalHeaderLabels(["RAW name", "PDCA name", "PDCA name_3"])

        # 表头加粗
        font = QFont()
        font.setBold(True)
        self.table_view.horizontalHeader().setFont(font)

        # 启用表头排序
        self.table_view.setSortingEnabled(True)

        # 交替行不同颜色
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setStyleSheet("QTableView { alternate-background-color: #f0f0f0; }")

        # 让列宽自适应窗口大小
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #开启线程
        monitor_thread = MonitorThread(pathroot=self.pathroot, dataGridView1=self.table_view)
        # monitor_thread.error_signal.connect(self.show_error_message)
        monitor_thread.start()
        
        # 创建按钮
        self.start_button = QPushButton("Start")
        self.setup_button = QPushButton("Setup")
        self.stop_button = QPushButton("Stop")

        # 连接 setup 按钮的点击事件
        self.setup_button.clicked.connect(self.open_setup_window)
        self.start_button.clicked.connect(lambda: self.start(monitor_thread))
        self.stop_button.clicked.connect(lambda: self.stop(monitor_thread))
        # 填充数据
        # data = self.data.T
        # for i in range(len(data)):
        #     for j in range(min(3, len(data.columns))):  # 确保不越界
        #         item = QStandardItem(str(data.iloc[i, j]))
        #         item.setEditable(False)
        #         self.model.setItem(i, j, item)

        # self.table_view.setModel(self.model)
        self.fo.load_format_from_local(self.table_view)
        # 设置布局
        main_layout = QVBoxLayout()
        button_layout = QGridLayout()

        # 添加按钮
        button_layout.addWidget(self.start_button, 0, 0)
        button_layout.addWidget(self.setup_button, 0, 2)
        button_layout.addWidget(self.stop_button, 0, 1)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table_view)

        self.setLayout(main_layout)
        
    def open_setup_window(self):
        """打开 Setup 窗口"""
        self.setup_window = SetupWindow(self)
        self.setup_window.setWindowModality(Qt.WindowModal)  # 设置模态窗口
        # self.setup_window.setWindowModality(Qt.WindowModal)  # 设置为模态窗口
        self.setup_window.show()
    def start(self,monitor_thread):
        if not os.path.exists(self.pathroot):
            self.show_error_message(f"路径 {self.pathroot} 不存在，请检查！")
            return
        monitor_thread.isrunning = True
    def stop(self,monitor_thread):
        monitor_thread.isrunning = False
    def show_error_message(self, msg):
        """ 这个方法会在主线程中执行 """
        QMessageBox.critical(self, "错误", msg)  # 让 GUI 线程弹出错误提示
    def load_system_setup(self):
        try:
            file_path = os.path.join(os.getcwd(), "systemsetup.txt")
            with open(file_path, "r", encoding="GBK") as f:
                lines = f.readlines()
            
            self.tcpip = lines[0].strip() if len(lines) > 0 else ""
            self.port = lines[1].strip() if len(lines) > 1 else ""
            self.pathroot = lines[2].strip() if len(lines) > 2 else ""  
        except Exception as e:
            print(f"Error: {e}")
    # def load_format_from_local(self, table_view):
    #     """ 加载本地 CSV 文件数据 """
    #     self.dynamic_list.clear()
    #     load_path = os.path.join(os.getcwd(), "Reflection_format.csv")
    #     if os.path.exists(load_path):
    #         self.dynamic_list_file_exists = True
    #         with open(load_path, "r", encoding="GBK") as f:
    #             reader = csv.reader(f)
    #             self.dynamic_list = [row for row in reader]
    #     else:
    #         self.dynamic_list_file_exists = False
    #         load_path = os.path.join(os.getcwd(), "DataFormat.csv")
    #         self.EQ_output_format = self.fo.read_para_csv(load_path)

    #     if self.dynamic_list_file_exists:
    #         self.fo.fill_table_view(table_view, self.dynamic_list)
    #     else:
    #         self.fo.fill_table_view(table_view, self.EQ_output_format)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataWindow()
    window.show()
    sys.exit(app.exec_())
