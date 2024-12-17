import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from VentanaEmpaquetado import VentanaProducto
from VentanaMetodoPago import VCashTypes
from VentanaVentaFinalizada import VSalesFinish


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RegistraBOT_Views")
        self.setFixedSize(600, 1020)
        #self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        # Inicializar la ventana de empaquetado
        self.vEmpaquetado = VentanaProducto()
        self.setCentralWidget(self.vEmpaquetado)

        # Conectar la señal del botón de registrar venta
        self.vEmpaquetado.botonregistrarVenta.clicked.connect(self.show_cash_types)

    def show_cash_types(self):
        # Mostrar la ventana de métodos de pago
        self.vCashTypes = VCashTypes(self)
        self.vCashTypes.show_in_center(self.vEmpaquetado.geometry())
        self.vCashTypes.show()

        # Conectar la señal de los botones de pago a la ventana de ventas finalizadas
        self.vCashTypes.buttonClicked.connect(self.show_sales_finish)

    def show_sales_finish(self):

        # Mostrar la ventana de venta finalizada
        self.vSalesFinish = VSalesFinish(self)
        self.vSalesFinish.show_in_center(self.vEmpaquetado.geometry())
        self.vSalesFinish.show()

        self.vCashTypes.close()
        # Conectar el botón de salir de VSalesFinish a VentanaProducto
        self.vSalesFinish.botonSalir.clicked.connect(self.show_empaquetado)

    def show_empaquetado(self):
        self.vSalesFinish.close()
        # Mostrar la ventana de empaquetado
        if self.vEmpaquetado.parent():
            self.vEmpaquetado.parent().setGraphicsEffect(None)
        self.vEmpaquetado.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())