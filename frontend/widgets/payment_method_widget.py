import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

parent_dir = '/home/pato/RegistraBot/frontend/assets/images'

class PaymentMethod(QDialog):

    buttonClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ventana Metodo de Pago")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(475, 667)
        self.setModal(True)

        # Bordes Redondos
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Widget principal con bordes redondeados
        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(0, 0, 475, 667)
        self.mainWidget.setStyleSheet("background-color: white; border-radius: 20px; color: black;")

        # Font Styles
        self.H1 = QFont("Tahoma", 21)
        self.H2 = QFont("Tahoma", 12, QFont.Bold)
        self.H3 = QFont("Tahoma", 11, QFont.Bold)
        self.H4 = QFont("Tahoma", 11)
        self.H5 = QFont("Tahoma", 19, QFont.Bold)
        self.H6 = QFont("Tahoma", 10)
        self.H7 = QFont("Tahoma", 16, QFont.Bold)
        self.H8 = QFont("Tahoma", 14, QFont.Bold)

        # Frame Center
        self.mainFrame = QWidget(self.mainWidget)
        self.mainFrame.setGeometry(62, 75, 352, 531)
        #self.mainFrame.setStyleSheet("background-color: white")
        self.layoutVC = QVBoxLayout(self.mainFrame)
        self.layoutVC.setContentsMargins(0, 0, 0, 0)

        # Text
        self.textLabel = QLabel('¿Con qué método de pago<br>vas a cobrar?', self.mainFrame)
        self.textLabel.setStyleSheet("color: #6C6C6C;")
        self.textLabel.setFixedSize(352, 58)
        self.textLabel.setFont(self.H3)
        self.textLabel.setAlignment(Qt.AlignCenter)

        # Monto Label
        self.frameMonto = QLabel(self.mainFrame)
        self.frameMonto.setFixedSize(352, 65)
        self.frameMontoHC = QHBoxLayout(self.frameMonto)

        self.labelMonto = QLabel('Pago total por:', self.frameMonto)
        self.labelMonto.setFont(self.H4)
        self.labelMonto.setStyleSheet("color: #6C6C6C;")
        self.labelMonto.setAlignment(Qt.AlignCenter)

        self.montoNum = QLabel('S/ 12.50', self.frameMonto)
        self.montoNum.setFont(self.H2)
        self.montoNum.setAlignment(Qt.AlignCenter)

        self.frameMontoHC.addWidget(self.labelMonto)
        self.frameMontoHC.addWidget(self.montoNum)

        # Frame de botones en una cuadrícula de 2x2
        self.frameGrid = QWidget(self.mainFrame)
        self.frameGridLayout = QGridLayout(self.frameGrid)
        self.frameGridLayout.setContentsMargins(0, 0, 0, 0)
        self.frameGridLayout.setSpacing(15)

        # Ajuste de tamaño para cada botón
        self.frameGrid.setFixedSize(352, 340)

        # Crear botones de método de pago
        self.create_payment_button('Yape', parent_dir + '/yapeImage.png', 0, 0)
        self.create_payment_button('Plin', parent_dir + '/plinImage.png', 0, 1)
        self.create_payment_button('Tarjeta', parent_dir + '/Credito.png', 1, 0)
        self.create_payment_button('Efectivo', parent_dir + '/Efectivo.png', 1, 1)

        # Agregar Widgets 
        self.layoutVC.addWidget(self.textLabel)
        self.layoutVC.addWidget(self.frameMonto)
        self.layoutVC.addWidget(self.frameGrid)

        # Posicionar la ventana al centro
        self.center_dialog()

    def create_payment_button(self, text, image_path, row, col):
        # Crear un QPushButton
        button = QPushButton(self.frameGrid)
        button.setFixedSize(142, 150)

        # Crear un layout vertical dentro del botón
        layout = QVBoxLayout(button)

        # Configurar el icono
        icon = QIcon(image_path)
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(85, 85))  # Tamaño del icono
        icon_label.setAlignment(Qt.AlignCenter)

        # Configurar el texto
        text_label = QLabel(text)
        text_label.setFont(self.H4)
        text_label.setStyleSheet("color: white;")
        text_label.setAlignment(Qt.AlignCenter)

        # Añadir el icono y el texto al layout
        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        # Estilo para el botón
        button.setStyleSheet("background-color: #B0CD3B; border-radius: 20px; color: white;")

        # Establecer el layout del botón
        button.setLayout(layout)

        # Agregar el botón a la cuadrícula
        self.frameGridLayout.addWidget(button, row, col)

        #button.clicked.connect(self.go_VentaFinalizada)
        button.clicked.connect(self.emit_button_clicked)

    def center_dialog(self):
        qr = self.frameGeometry()
        cp = self.parent().geometry().center() if self.parent() else QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_in_center(self, parent_geometry):
        self_geometry = self.geometry()
        x = parent_geometry.x() + (parent_geometry.width() - self_geometry.width()) // 2
        y = parent_geometry.y() + (parent_geometry.height() - self_geometry.height()) // 2
        self.move(x, y)

        if self.parent():
            blur_effect = QGraphicsBlurEffect()
            blur_effect.setBlurRadius(10)
            self.parent().setGraphicsEffect(blur_effect)

        self.show()

    def emit_button_clicked(self):
        self.buttonClicked.emit()