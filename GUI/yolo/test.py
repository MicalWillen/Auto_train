import sys
import os
import paramiko
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTreeView, QPushButton, QFileSystemModel, QMessageBox, QComboBox, QListWidget, QLineEdit
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon

class FileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件管理器")

        # 当前路径显示
        self.current_path = "/home"  # 假设初始路径是本地或远程路径
        self.path_label = QLabel(self.current_path)

        # 本地与远程路径区分标志
        self.is_local = True  # 默认是本地路径
        self.ssh_client = None
        self.sftp_client = None
        self.remote_server = "10.10.8.206"  # 替换为你的远程服务器IP
        self.username = "root"  # 替换为用户名
        self.password = "Amax1979!"  # 替换为密码

        self.history = []
        self.current_index = -1
        self.listWidget = QListWidget()  # 假设你有一个 QListWidget 用于显示文件列表
        self.lineEdit = QLineEdit()  # 假设你有一个 QLineEdit 用于输入路径

        # 文件列表
        self.file_list = QTreeView()
        self.model = QFileSystemModel()
        self.file_list.setModel(self.model)
        self.file_list.doubleClicked.connect(self.open_file_or_directory)  # 双击打开

        # 按钮
        self.back_button = QPushButton("返回")
        self.back_button.clicked.connect(self.go_back)

        # 布局
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("路径："))
        path_layout.addWidget(self.path_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(path_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.file_list)

        self.setLayout(main_layout)

        # 连接远程服务器
        self.connect_to_remote_server()

    def connect_to_remote_server(self):
        """连接到远程服务器"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.remote_server, username=self.username, password=self.password)
            self.sftp_client = self.ssh_client.open_sftp()
            self.load_remote_files(self.current_path)
        except Exception as e:
            QMessageBox.critical(self, "连接失败", f"无法连接到远程服务器: {str(e)}")

    def load_remote_files(self, path):
        """加载远程目录中的文件"""
        try:
            remote_files = self.sftp_client.listdir(path)
            self.current_path = path
            self.path_label.setText(self.current_path)
            self.update_file_list(remote_files)
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"无法加载远程文件: {str(e)}")

    def load_local_files(self, path):
        """加载本地目录中的文件"""
        local_files = os.listdir(path)
        self.current_path = path
        self.path_label.setText(self.current_path)
        self.update_file_list(local_files)

    def update_file_list(self, files):
        """更新文件列表"""
        self.file_list.setRootIndex(self.model.index(self.current_path))
        # 这里只是一个示例，假设我们手动更新文件列表，可以进行进一步的封装。

    def open_file_or_directory(self, index):
        """打开文件或目录"""
        path = self.model.filePath(index)
        
        if self.is_local:
            # 本地文件操作
            if os.path.isdir(path):
                self.load_local_files(path)
            else:
                QMessageBox.information(self, "文件", f"打开本地文件：{path}")
        else:
            # 远程文件操作
            try:
                if self.sftp_client.isdir(path):
                    self.load_remote_files(path)
                else:
                    QMessageBox.information(self, "文件", f"尝试打开远程文件：{path}")
            except Exception as e:
                QMessageBox.critical(self, "打开失败", f"无法打开文件或目录: {str(e)}")

    def go_back(self):
        """返回到上一级目录"""
        if self.is_local:
            parent_path = os.path.dirname(self.current_path)
            if parent_path != self.current_path:
                self.load_local_files(parent_path)
        else:
            if self.current_path != "/":
                parent_path = os.path.dirname(self.current_path)
                self.load_remote_files(parent_path)
            else:
                QMessageBox.information(self, "提示", "已到达根目录，无法返回更上层")

    def closeEvent(self, event):
        """关闭时断开与服务器的连接"""
        if self.sftp_client:
            self.sftp_client.close()
        if self.ssh_client:
            self.ssh_client.close()

    def yolo(self):
        """通过 SSH 连接到远程服务器并列出文件和目录"""
        input_text = self.lineEdit.text()
        
        hostname = '10.10.8.201'
        port = 22
        username = 'root'
        password = 'Amax1979!'
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(hostname, port, username, password)
            stdin, stdout, stderr = ssh.exec_command(f'ls -p {input_text}')
            items = stdout.readlines()
            
            self.listWidget.clear()
            for item in items:
                self.listWidget.addItem(item.strip())
            
            if self.current_index == -1 or self.history[self.current_index] != input_text:
                self.history = self.history[:self.current_index + 1]
                self.history.append(input_text)
                self.current_index += 1
        
        except Exception as e:
            self.statusbar.showMessage(f"Connection failed: {str(e)}")
        
        finally:
            ssh.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())
