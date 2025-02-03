# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from frontend.ui.main_window import DetectionWindows
from frontend.widgets.payment_method_widget import PaymentMethod
from frontend.widgets.sale_completion_widget import SaleCompletion
from frontend.widgets.report_method_widget import ReportMethod


class MainWindow_RB(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RegistraBOT")
        self.setFixedSize(600, 1024)
        #self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        # Inicializar la ventana de empaquetado
        self.vEmpaquetado = DetectionWindows()
        self.setCentralWidget(self.vEmpaquetado)

        # Conectar la senal del boton de registrar venta
        self.vEmpaquetado.botonregistrarVenta.clicked.connect(self.show_cash_types)
        
    def show_cash_types(self):
        # Mostrar la ventana de métodos de pago
        self.vCashTypes = PaymentMethod(self)
        self.vCashTypes.show_in_center(self.vEmpaquetado.geometry())
        self.vCashTypes.show()

        # Conectar la señal de los botones de pago a la ventana de ventas finalizadas
        self.vCashTypes.buttonClicked.connect(self.show_sales_finish)

    def show_sales_finish(self):

        # Mostrar la ventana de venta finalizada
        self.vSalesFinish = SaleCompletion(self)
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
    main_window = MainWindow_RB()
    main_window.show()
    sys.exit(app.exec_())