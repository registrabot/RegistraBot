## VLoadData.py

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class VLoadData(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Progress Dialog")
        self.setStyleSheet("background-color: white; border-radius: 10px; color: black;")
        self.setFixedSize(400, 240)
        self.setModal(True)

        # Remove close, minimize, and maximize buttons
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.FramelessWindowHint)

        # Create a rounded rectangle mask using QPixmap and QBitmap
        radius = 15
        mask = QBitmap(self.size())
        mask.fill(Qt.white)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.drawRoundedRect(self.rect(), radius, radius)
        painter.end()
        self.setMask(mask)

        self.center_dialog()

        self.H7 = QFont("Tahoma", 16)

        self._loadBlock_wgt = QWidget(self)
        self._loadBlock_wgt.setStyleSheet("background-color: white; border-radius: 30px; color: black;")
        self.layoutVC = QVBoxLayout(self._loadBlock_wgt)
        self.layoutVC.setContentsMargins(60, 90, 60, 90)

        self.label_bar = QLabel('Subiendo datos', self._loadBlock_wgt)
        self.label_bar.setFont(self.H7)
        self.label_bar.setStyleSheet("background-color: white; color: #6C6C6C;")
        self.label_bar.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar(self._loadBlock_wgt)
        self.progress_bar.setStyleSheet("background-color: green; color: #6C6C6C;")
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 0px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #FF8811;
                width: 20px;
            }
        """)

        self.layoutVC.addWidget(self.label_bar)
        self.layoutVC.addWidget(self.progress_bar)

        self.setLayout(self.layoutVC)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(30)

    def center_dialog(self):
        qr = self.frameGeometry()
        cp = self.parent().geometry().center() if self.parent() else QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_progress_bar(self):
        value = self.progress_bar.value()
        value += 1

        if value > 100:
            self.accept()  # Close the dialog when progress reaches 100%
        else:
            self.progress_bar.setValue(value)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z:
            self.show()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = VLoadData()
    dialog.show()
    sys.exit(app.exec_())