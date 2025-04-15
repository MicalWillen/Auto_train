from PyQt5.QtCore import QThread, pyqtSignal
import os

class MonitorThread(QThread):  # 确保继承 QThread
    error_signal = pyqtSignal(str)  # 定义信号

    def __init__(self, pathroot):
        super().__init__()  # 确保 QThread 正确初始化
        self.pathroot = pathroot

    def run(self):
        """ 线程运行逻辑 """
        if not os.path.exists(self.pathroot):
            self.error_signal.emit(f"路径 {self.pathroot} 不存在，请检查！")  # 发送信号
