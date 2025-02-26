import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class NumericKeyboard(QWidget):
    numero_actualizado = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal del widget
        self.setWindowTitle("Teclado Numerico Widget")
        self.setFixedSize(600, 566)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Font Styles
        self.H1 = QFont("Tahoma", 21)
        self.H2 = QFont("Tahoma", 12, QFont.Bold)
        self.H3 = QFont("Tahoma", 11)
        self.H4 = QFont("Tahoma", 9)
        self.H5 = QFont("Tahoma", 19, QFont.Bold)
        self.H6 = QFont("Tahoma", 10)
        self.H7 = QFont("Tahoma", 14)
        self.H8 = QFont("Tahoma", 16)

        # Almacenar los números presionados
        self.numeros_presionados = []

        # Teclado Númerico
        self.widgetCentral = QLabel(self)
        self.widgetCentral.setGeometry(0, 0, 600, 566)
        self.widgetCentral.setStyleSheet("background-color: #D9D9D9; border-top-left-radius: 20px; border-top-right-radius: 20px;")

        self.teclado = QLabel(self.widgetCentral)
        self.teclado.setGeometry(110, 69, 363, 457)
        self.tecladoVC = QVBoxLayout(self.teclado)
        self.tecladoVC.setContentsMargins(0, 0, 0, 0)

        # Primera Fila
        self.tecladoprimera = QLabel(self.teclado)
        self.tecladoprimera.setFixedSize(363, 77)
        self.tecladoprimeraHC = QHBoxLayout(self.tecladoprimera)
        self.tecladoprimeraHC.setContentsMargins(0, 0, 0, 0)

        self.tecladosegunda = QLabel(self.teclado)
        self.tecladosegunda.setFixedSize(363, 75)
        self.tecladosegundaHC = QHBoxLayout(self.tecladosegunda)
        self.tecladosegundaHC.setContentsMargins(0, 0, 0, 0)

        self.tecladotercera = QLabel(self.teclado)
        self.tecladotercera.setFixedSize(363, 75)
        self.tecladoterceraHC = QHBoxLayout(self.tecladotercera)
        self.tecladoterceraHC.setContentsMargins(0, 0, 0, 0)

        self.tecladocuarta = QLabel(self.teclado)
        self.tecladocuarta.setFixedSize(363, 77)
        self.tecladocuartaHC = QHBoxLayout(self.tecladocuarta)
        self.tecladocuartaHC.setContentsMargins(0, 0, 0, 0)

        # Botones
        self.boton1 = QPushButton("1", self.tecladoprimera)
        self.boton1.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton1.setFont(self.H8)
        self.boton1.setFixedSize(114, 77)
        self.boton1.clicked.connect(lambda: self.guardar_numero(1))

        self.boton2 = QPushButton("2", self.tecladoprimera)
        self.boton2.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton2.setFont(self.H8)
        self.boton2.setFixedSize(114, 77)
        self.boton2.clicked.connect(lambda: self.guardar_numero(2))

        self.boton3 = QPushButton("3", self.tecladoprimera)
        self.boton3.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton3.setFont(self.H8)
        self.boton3.setFixedSize(114, 77)
        self.boton3.clicked.connect(lambda: self.guardar_numero(3))

        self.boton4 = QPushButton("4", self.tecladosegunda)
        self.boton4.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton4.setFont(self.H8)
        self.boton4.setFixedSize(114, 77)
        self.boton4.clicked.connect(lambda: self.guardar_numero(4))

        self.boton5 = QPushButton("5", self.tecladosegunda)
        self.boton5.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton5.setFont(self.H8)
        self.boton5.setFixedSize(114, 77)
        self.boton5.clicked.connect(lambda: self.guardar_numero(5))

        self.boton6 = QPushButton("6", self.tecladosegunda)
        self.boton6.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton6.setFont(self.H8)
        self.boton6.setFixedSize(114, 77)
        self.boton6.clicked.connect(lambda: self.guardar_numero(6))

        self.boton7 = QPushButton("7", self.tecladotercera)
        self.boton7.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton7.setFont(self.H8)
        self.boton7.setFixedSize(114, 77)
        self.boton7.clicked.connect(lambda: self.guardar_numero(7))

        self.boton8 = QPushButton("8", self.tecladotercera)
        self.boton8.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton8.setFont(self.H8)
        self.boton8.setFixedSize(114, 77)
        self.boton8.clicked.connect(lambda: self.guardar_numero(8))

        self.boton9 = QPushButton("9", self.tecladotercera)
        self.boton9.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton9.setFont(self.H8)
        self.boton9.setFixedSize(114, 77)
        self.boton9.clicked.connect(lambda: self.guardar_numero(9))

        self.botonSalir = QPushButton("Salir", self.tecladotercera)
        self.botonSalir.setStyleSheet("background-color: red; color: white; border-radius: 10px;")
        self.botonSalir.setFont(self.H7)
        self.botonSalir.setFixedSize(114, 77)

        # Conectar el botón Salir para cerrar el teclado
        #self.botonSalir.clicked.connect(self.close_teclado)

        self.boton0 = QPushButton("0", self.tecladotercera)
        self.boton0.setStyleSheet("background-color: #8C8C8C; color: white; border-radius: 10px;")
        self.boton0.setFont(self.H8)
        self.boton0.setFixedSize(114, 77)
        self.boton0.clicked.connect(lambda: self.guardar_numero(0))

        self.botonBorrar = QPushButton("Borrar", self.tecladotercera)
        self.botonBorrar.setStyleSheet("background-color: red; color: white; border-radius: 10px;")
        self.botonBorrar.setFont(self.H7)
        self.botonBorrar.setFixedSize(114, 77)
        self.botonBorrar.clicked.connect(self.borrar_ultimo)

        self.botonAniadir = QPushButton("Añadir al Carrito", self.teclado)
        self.botonAniadir.setStyleSheet("background-color: #639C3B; color: white; border-radius: 15px;")
        self.botonAniadir.setFont(self.H7)
        self.botonAniadir.setFixedSize(363, 64)

        self.tecladoprimeraHC.addWidget(self.boton1)
        self.tecladoprimeraHC.addWidget(self.boton2)
        self.tecladoprimeraHC.addWidget(self.boton3)

        self.tecladosegundaHC.addWidget(self.boton4)
        self.tecladosegundaHC.addWidget(self.boton5)
        self.tecladosegundaHC.addWidget(self.boton6)

        self.tecladoterceraHC.addWidget(self.boton7)
        self.tecladoterceraHC.addWidget(self.boton8)
        self.tecladoterceraHC.addWidget(self.boton9)

        self.tecladocuartaHC.addWidget(self.botonSalir)
        self.tecladocuartaHC.addWidget(self.boton0)
        self.tecladocuartaHC.addWidget(self.botonBorrar)

        self.tecladoVC.addWidget(self.tecladoprimera)
        self.tecladoVC.addWidget(self.tecladosegunda)
        self.tecladoVC.addWidget(self.tecladotercera)
        self.tecladoVC.addWidget(self.tecladocuarta)
        self.tecladoVC.addWidget(self.botonAniadir)

        # Atajo de teclado para cerrar la ventana con Ctrl + C
        shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        shortcut.activated.connect(self.close)

    def guardar_numero(self, numero):
        if len(self.numeros_presionados) < 6:
            self.numeros_presionados.append(str(numero))
        self.numero_actualizado.emit(''.join(self.numeros_presionados))
        

    def borrar_ultimo(self):
        # Borra el último número ingresado
        self.numeros_presionados = self.numeros_presionados[:-1]
        self.numero_actualizado.emit(''.join(self.numeros_presionados))

    def reset_keyboard(self):
        self.numeros_presionados = []
