## VentanaVentaFinalizada.py

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
import sqlite3
#from ticketprinter_module.TicketPrinterClass import TicketPrinter
import numpy as np

class VSalesFinish(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ventana Venta Finalizada")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(475, 600)
        self.setModal(True)

        # Bordes Redondos
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Widget principal con bordes redondeados
        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(0, 0, 475, 600)
        self.mainWidget.setStyleSheet("background-color: white; border-radius: 20px; color: black;")

        # Font Styles
        self.H1 = QFont("Tahoma", 21)
        self.H2 = QFont("Tahoma", 12, QFont.Bold)
        self.H3 = QFont("Tahoma", 11)
        self.H4 = QFont("Tahoma", 9)
        self.H5 = QFont("Tahoma", 19, QFont.Bold)
        self.H6 = QFont("Tahoma", 10)
        self.H7 = QFont("Tahoma", 16, QFont.Bold)
        self.H8 = QFont("Tahoma", 14, QFont.Bold)

        # Frame Center
        self.mainFrame = QWidget(self.mainWidget)
        self.mainFrame.setGeometry(65, 109, 345, 381)
        self.mainFrame.setStyleSheet("background-color: white; border-radius: 20px;")
        self.layoutVC = QVBoxLayout(self.mainFrame)
        self.layoutVC.setContentsMargins(0, 0, 0, 0)

        # Image
        self.imageCheck = QLabel(self.mainFrame)
        self.imageCheck.setPixmap(QPixmap("../Imagenes/CheckCircleFill.png"))
        self.imageCheck.setAlignment(Qt.AlignCenter)

        # Label
        self.labelVenta = QLabel('Venta registrada', self.mainFrame)
        self.labelVenta.setFont(self.H8)
        self.labelVenta.setAlignment(Qt.AlignCenter)

        # Boton Imprimir
        self.botonImprimir = QPushButton("Imprimir Voucher", self.mainFrame)
        self.botonImprimir.setFixedSize(345,64)
        self.botonImprimir.setFont(self.H2)
        self.botonImprimir.setAutoFillBackground(False)
        self.botonImprimir.setStyleSheet("background-color: #639C3B; color: white; border-radius: 15px;")
        self.botonImprimir.setIcon(QIcon("../Imagenes/Sticky.png"))
        self.botonImprimir.setIconSize(QSize(44, 44))
        self.botonImprimir.setFlat(True)
        self.botonImprimir.setLayoutDirection(Qt.RightToLeft)
        self.botonImprimir.clicked.connect(self.imprimir_voucher)

        # Boton Salir
        self.botonSalir = QPushButton("Salir", self.mainFrame)
        self.botonSalir.setFixedSize(345,64)
        self.botonSalir.setFont(self.H2)
        self.botonSalir.setAutoFillBackground(False)
        self.botonSalir.setStyleSheet("background-color: #939393; color: white; border-radius: 15px;")
        self.botonSalir.setIcon(QIcon("../Imagenes/X.png"))
        self.botonSalir.setIconSize(QSize(44, 44))
        self.botonSalir.setFlat(True)
        self.botonSalir.setLayoutDirection(Qt.RightToLeft)

        # Agregar Widgets 
        self.layoutVC.addWidget(self.imageCheck)
        self.layoutVC.addSpacing(30)
        self.layoutVC.addWidget(self.labelVenta)
        self.layoutVC.addSpacing(50)
        self.layoutVC.addWidget(self.botonImprimir)
        self.layoutVC.addSpacing(25)
        self.layoutVC.addWidget(self.botonSalir)


        # Posicionar la ventana al centro
        self.center_dialog()

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
    
    def imprimir_voucher(self):
        return print('imprimir')
