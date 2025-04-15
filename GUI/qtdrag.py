import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class DraggableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black; padding: 10px;")
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)

        drag.exec_(Qt.MoveAction)

class DropArea(QLabel):
    def __init__(self, parent=None):
        super().__init__("Drop here", parent)
        self.setStyleSheet("background-color: lightgrey; border: 1px solid black; padding: 10px;")
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        text = event.mimeData().text()
        self.setText(f"Dropped: {text}")
        event.acceptProposedAction()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.draggable_label = DraggableLabel("Drag me")
        self.drop_area = DropArea()

        layout.addWidget(self.draggable_label)
        layout.addWidget(self.drop_area)

        self.setLayout(layout)
        self.setWindowTitle("Drag and Drop Example")
        self.setGeometry(300, 300, 300, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())