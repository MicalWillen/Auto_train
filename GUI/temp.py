import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, QAction, QWidget)
from PyQt5.QtCore import QCoreApplication

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("新窗口")
        # 在这里添加新窗口的布局和控件

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("菜单栏示例")

        # 创建菜单栏
        menubar = self.menuBar()

        # 创建文件菜单
        self.file_menu = menubar.addMenu("文件")

        # 创建新建菜单项
        # new_action = QAction("", self)
        # self.file_menu.addAction(new_action)

        # 连接信号与槽
        # new_action.triggered.connect(self.open_new_window)

        # 连接文件菜单的 aboutToShow 信号
        self.file_menu.aboutToShow.connect(self.open_new_window)

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())