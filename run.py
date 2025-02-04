# -*- coding: utf-8 -*-
import sys
from time import sleep
import sqlite3
import datetime
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
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()

        self.product_list = []
        self.id_bodega = 12345

        # Inicializar la ventana de empaquetado
        self.vEmpaquetado = DetectionWindows()
        self.setCentralWidget(self.vEmpaquetado)

        # Conectar la senal del boton de registrar venta
        self.vEmpaquetado.botonregistrarVenta.clicked.connect(self.show_cash_types)
        
    def show_cash_types(self):
        # Mostrar la ventana de métodos de pago
        self.vCashTypes = PaymentMethod(self)
        self.vCashTypes.set_product_list(self.vEmpaquetado.listProductWidget.get_products_list())
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
        self.vSalesFinish.botonFinalizar.clicked.connect(lambda: self.upload_sell_data(self.vCashTypes.products))


    def show_empaquetado(self):
        self.vEmpaquetado.reset_product_info()
        self.vSalesFinish.close()
        # Mostrar la ventana de empaquetado
        if self.vEmpaquetado.parent():
            self.vEmpaquetado.parent().setGraphicsEffect(None)
        self.vEmpaquetado.show()

    
    def upload_sell_data(self, product_list):
    
        db_path = '/home/pato/RegistraBot/backend/database/BD_RegistraBOT.db'
        DB_connector = sqlite3.connect(db_path)
        cursor = DB_connector.cursor()

        id_venta = 0

        cursor.execute('SELECT MAX(id_venta) FROM tb_registro_ventas')
        last_id_venta = cursor.fetchone()

        try:
            if len(last_id_venta) > 0:
                id_venta = int(last_id_venta[0]+ 1)
            else:
                id_venta = int(0)
        except:
            id_venta = int(0)
        
        for producto in product_list:
            item = [] # id_venta, id_bodega, sku, cantidad, precio_unitario, precio_total, medio_pago

            item.append(id_venta)
            item.append(str(self.id_bodega))
            item.append(producto['sku'])  # SKU
            item.append(int(producto['quantity']))  # cantidad
            item.append(float(producto['unit_price']))  # precio_unitario
            item.append(float(producto['total_price']))  # precio_total
            item.append(producto.get('medio_pago'))  # medio_pago
            item.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # insert_date
            item.append(int(0)) # estado_carga

            cursor.executemany('INSERT INTO tb_registro_ventas (id_venta, id_bodega, sku, cantidad, precio_unitario, precio_total, medio_pago, insert_date, estado_carga) VALUES (?,?,?,?,?,?,?,?,?)', [tuple(item)])
            DB_connector.commit()
        DB_connector.close()

        self.show_empaquetado()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow_RB()
    main_window.show()
    sys.exit(app.exec_())