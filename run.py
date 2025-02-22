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
import requests
import json
import time
from datetime import datetime


# Configuración de ThingsBoard
THINGSBOARD_HOST = 'https://thingsboard.cloud'
ACCESS_TOKEN = 'lGJjHAKOtOfGMkgkoMJK'
TELEMETRY_URL = f"{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry"
DB_PATH = '/home/pato/RegistraBot/backend/database/BD_RegistraBOT.db'

def send_telemetry(data):
    """ Envía datos a ThingsBoard """
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(TELEMETRY_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"✔ Telemetría enviada correctamente: {data}")
        else:
            print(f"❌ Error al enviar telemetría: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠ Error enviando telemetría: {e}")

def send_data():
    """ Obtiene datos de la BD y los envía a ThingsBoard """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = '''SELECT * FROM tb_registro_ventas A 
                   LEFT JOIN tb_catalogo_productos B 
                   ON TRIM(REPLACE(REPLACE(A.sku, '\n', ''), '\r', '')) = B.sku 
                   WHERE A.estado_carga = 0'''
        cursor.execute(query)
        tb_catalogo_productos = cursor.fetchall()

        if not tb_catalogo_productos:
            print("✅ No hay nuevos datos para enviar.")
            return

        for producto in tb_catalogo_productos:
            data = [{
                'ts': int(datetime.now().timestamp()*1000),
                'values': {
                    'id': producto[0],
                    'id_venta': producto[1],
                    'id_bodega': producto[2],
                    'sku': producto[3],
                    'cantidad': producto[4],
                    'precio_unitario': producto[5],
                    'precio_total': producto[6],
                    'medio_pago': producto[7],
                    'date': producto[8]
                }
            }]

            print(f"📤 Enviando: {data}")
            send_telemetry(data)

            update_query = '''UPDATE tb_registro_ventas SET estado_carga = 1 WHERE id = ?'''
            cursor.execute(update_query, (producto[0],))
            time.sleep(0.5)

        conn.commit()
        print("✅ Envío de datos completado.")

    except Exception as e:
        print(f"❌ Error procesando datos: {e}")

    finally:
        conn.close()

def start_timer():
    """ Inicia un temporizador que revisa la hora cada minuto """
    timer = QTimer()
    timer.timeout.connect(check_time)
    timer.start(60000)  # Verifica la hora cada 60 segundos
    print("⏳ Temporizador iniciado para revisar la hora cada minuto.")
    return timer

def check_time():
    """ Revisa si son las 10:40 PM (22:40) y ejecuta el envío """
    now = datetime.now()
    #print(f"HORA: {now.hour}, Minuto: {now.minute}")  # Debug
    if now.hour == 12 and now.minute == 00:
        print("⏳ Ejecutando envío de datos a ThingsBoard...")
        send_data()
        print("✅ Datos enviados a ThingsBoard.")


class MainWindow_RB(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RegistraBOT")
        self.setFixedSize(600, 1024)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()

        self.product_list = []
        self.id_bodega = 75331797

        # Inicializar la ventana de empaquetado
        self.vEmpaquetado = DetectionWindows()
        self.setCentralWidget(self.vEmpaquetado)
        #self.timer = start_timer()  # Inicia el temporizador en segundo plano
        # Conectar la senal del boton de registrar venta
        self.vEmpaquetado.botonregistrarVenta.clicked.connect(self.show_cash_types)
        
    def show_cash_types(self):
        product_list = self.vEmpaquetado.listProductWidget.get_products_list()
        if len(product_list) == 0:
            return
        # Mostrar la ventana de métodos de pago
        self.vCashTypes = PaymentMethod(self)
        self.vCashTypes.set_product_list(product_list)
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
            item.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # insert_date
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
