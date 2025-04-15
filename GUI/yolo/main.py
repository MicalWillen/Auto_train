import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 140, 341, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Run YOLO")
        self.pushButton.clicked.connect(self.yolo)
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 140, 321, 20))
        self.lineEdit.setObjectName("lineEdit")
        
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 180, 681, 361))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.open_directory)
        
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(20, 100, 75, 23))
        self.backButton.setObjectName("backButton")
        self.backButton.setText("Back")
        self.backButton.clicked.connect(self.go_back)
        
        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.forwardButton.setObjectName("forwardButton")
        self.forwardButton.setText("Forward")
        self.forwardButton.clicked.connect(self.go_forward)
        
        self.rootButton = QtWidgets.QPushButton(self.centralwidget)
        self.rootButton.setGeometry(QtCore.QRect(180, 100, 75, 23))
        self.rootButton.setObjectName("rootButton")
        self.rootButton.setText("Root")
        self.rootButton.clicked.connect(self.open_root)
        
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(260, 100, 75, 23))
        self.browseButton.setObjectName("browseButton")
        self.browseButton.setText("Browse")
        self.browseButton.clicked.connect(self.browse_directory)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        
        self.history = []
        self.current_index = -1

    def yolo(self):
        # Get the input from the line edit
        input_text = self.lineEdit.text()
        
        # SSH connection details
        hostname = '10.10.8.201'
        port = 22
        username = 'root'
        password = 'Amax1979!'
        
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # Connect to the server
            ssh.connect(hostname, port, username, password)
            
            # Execute the command to list files and directories
            stdin, stdout, stderr = ssh.exec_command(f'ls -p {input_text}')
            items = stdout.readlines()
            
            # Clear the list widget
            self.listWidget.clear()
            
            # Add items to the list widget
            for item in items:
                self.listWidget.addItem(item.strip())
            
            # Update history
            if self.current_index == -1 or self.history[self.current_index] != input_text:
                self.history = self.history[:self.current_index + 1]
                self.history.append(input_text)
                self.current_index += 1
        
        except Exception as e:
            self.statusbar.showMessage(f"Connection failed: {str(e)}")
        
        finally:
            # Close the SSH connection
            ssh.close()


    def open_directory(self, item):
        directory = item.text()
        self.lineEdit.setText(directory)
        self.yolo()

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.lineEdit.setText(self.history[self.current_index])
            self.yolo()

    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.lineEdit.setText(self.history[self.current_index])
            self.yolo()

    def open_root(self):
        self.lineEdit.setText('/')
        self.yolo()

    def browse_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        if directory:
            self.lineEdit.setText(directory)
            self.yolo()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
