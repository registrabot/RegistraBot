import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
import sqlite3

parent_dir = '/home/pato/RegistraBot/backend/modules'
sys.path.append(parent_dir)
from backend.modules.barcode_module.barcode_module import ScannerThread

parent_dir = '/home/pato/RegistraBot/frontend/'
sys.path.append(parent_dir)
from widgets.numeric_keyboard_widget import NumericKeyboard
from widgets.shopping_cart_widget import ShoppingCart
from widgets.report_method_widget import ReportMethod
from widgets.payment_method_widget import PaymentMethod

class DetectionWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600, 1020)
        self.setWindowTitle("Ventana Producto")
        self.setStyleSheet("background-color: #EEEEEE;")
        
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.product_sku = ""
        self.product_name = ""
        self.product_img_path = ""
        self.product_isBulk = True
        self.product_quantity = 1
        self.product_weight = 0.5
        self.product_price = 0
        self.ventana_metodoPago = PaymentMethod()

        # Connect Database
        self.db_path = '/home/pato/RegistraBot/backend/database/BD_RegistraBOT.db'
        self.connection = self.connect_to_database()

        # Init Variables
        self.input_digits = ""      

        # Font Styles
        self.H1 = QFont("Tahoma", 21)
        self.H2 = QFont("Tahoma", 12, QFont.Bold)
        self.H3 = QFont("Tahoma", 11)
        self.H4 = QFont("Tahoma", 9)
        self.H5 = QFont("Tahoma", 19, QFont.Bold)
        self.H6 = QFont("Tahoma", 10)
        self.H7 = QFont("Tahoma", 16, QFont.Bold)
        self.H8 = QFont("Tahoma", 14, QFont.Bold)

        # Main Frame
        self.mainFrame = QFrame(self)
        self.mainFrame.setGeometry(0,0,600,1020) 
        self.layoutVC = QVBoxLayout(self.mainFrame)
        self.layoutVC.setContentsMargins(0, 0, 0, 0)

        # Detection Panel (Frame)
        self.frameDetectionPanel = QLabel(self.mainFrame)
        self.frameDetectionPanel.setGeometry(0, 0, 600, 427)
        self.frameDetectionPanel.setPixmap(QPixmap(parent_dir + "/assets/images/Supermercado.png"))
        self.frameDetectionPanel.setScaledContents(True)
        
        self.frameDetectionPanelVC = QVBoxLayout(self.frameDetectionPanel)
        self.frameDetectionPanelVC.setContentsMargins(31, 45, 31, 26)

        # Bar Frame
        self.frameBar = QLabel(self.frameDetectionPanel)
        self.frameBar.setFixedSize(533, 25)
        self.frameBar.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.frameBarHC = QHBoxLayout(self.frameBar)
        self.frameBarHC.setContentsMargins(0, 0, 0, 0)

        # Rb Image
        self.rbImageBar = QLabel(self.frameBar)
        self.rbImageBar.setPixmap(QPixmap(parent_dir + "/assets/images/logoRb.png"))
        self.rbImageBar.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # Rb Label
        self.rbLabelBar = QLabel('RegistraBOT', self.frameBar)
        self.rbLabelBar.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: white;")
        self.rbLabelBar.setFont(self.H2)

        # Rb Time Label
        self.rbTimeBar = QLabel('', self.frameBar)
        self.rbTimeBar.setFont(self.H3)
        self.rbTimeBar.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: white;")
        self.update_clock()

        # Add widgets to the bar layout
        self.frameBarHC.addWidget(self.rbImageBar)
        self.frameBarHC.addSpacing(1)
        self.frameBarHC.addWidget(self.rbLabelBar)
        self.frameBarHC.addSpacing(290)
        self.frameBarHC.addWidget(self.rbTimeBar)

        # LabelProductName
        self.frameProductLabel = QHBoxLayout(self.frameDetectionPanel)
        self.productName = QLabel(self.product_name, self.frameDetectionPanel)
        self.productName.setFixedSize(420, 50)
        self.productName.setStyleSheet("background-color: rgba(255, 255, 255, 180); color: black; border-radius: 10px;")
        self.productName.setFont(self.H2)

        # Start Detection Button
        self.scanner_thread = ScannerThread()
        self.botonDashboard = QPushButton("Reporte", self.frameDetectionPanel)
        self.botonDashboard.setFixedSize(110,50)
        self.botonDashboard.setFont(self.H2)
        self.botonDashboard.setFlat(True)
        self.botonDashboard.setStyleSheet("background-color: #639C3B; color: white; border-radius: 15px;")

        self.frameProductLabel.addWidget(self.productName)
        self.frameProductLabel.addWidget(self.botonDashboard)

        self.botonDashboard.clicked.connect(self.verDashboard)

        self.scanner_thread.scanned_signal.connect(self.barcode_scanned)
        if not self.scanner_thread.isRunning():
            self.scanner_thread.start()
        
        # Box : Image + Items
        self.boxProduct = QLabel(self.frameDetectionPanel)
        self.boxProduct.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.boxProductHC = QHBoxLayout(self.boxProduct)
        self.boxProductHC.setContentsMargins(0, 0, 0, 0)

            # Image Product
        self.imageBoxProduct = QLabel(self.boxProduct)
        self.imageBoxProduct.setFixedSize(210,220)
        self.imageBoxProduct.setPixmap(QPixmap("backend/database/product_images/NO-FOUND.png"))

            # Items Product
        self.itemsProduct = QLabel(self.boxProduct)
        self.itemsProduct.setFixedSize(309,226)
        self.itemsProductVC = QVBoxLayout(self.itemsProduct)
        self.itemsProductVC.setContentsMargins(0, 0, 0, 0)

            # Peso Label
        self.framePeso = QLabel(self.itemsProduct)
        self.framePeso.setFixedSize(309,60)
        self.framePesoHC = QHBoxLayout(self.framePeso)
        self.framePesoHC.setContentsMargins(0, 0, 0, 0)

            # Precio x kg Label
        self.framePrecio = QLabel(self.itemsProduct)
        self.framePrecio.setFixedSize(309,60)
        self.framePrecioHC = QHBoxLayout(self.framePrecio)
        self.framePrecioHC.setContentsMargins(0, 0, 0, 0)

        self.precioName = QLabel('Precio x Kg', self.framePrecio)
        self.precioName.setFixedSize(115,20)
        self.precioName.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: white;")
        self.precioName.setFont(self.H2)

        self.precioValue = QLabel('S/ 0.00', self.framePrecio)
        self.precioValue.setFixedSize(174,45)
        self.precioValue.setStyleSheet("background-color: rgba(255, 255, 255); color: black; border-radius: 10px;")
        self.precioValue.setFont(self.H3)
        self.precioValue.setAlignment(Qt.AlignCenter)
        self.precioValue.mousePressEvent = self.mostrar_teclado

        self.framePrecioHC.addWidget(self.precioName)
        self.framePrecioHC.addWidget(self.precioValue)
        
            # SubTotal Label
        self.frameSubTotal = QLabel(self.itemsProduct)
        self.frameSubTotal.setFixedSize(309,60)
        self.frameSubTotalHC = QHBoxLayout(self.frameSubTotal)
        self.frameSubTotalHC.setContentsMargins(0, 0, 0, 0)

        self.subTotalName = QLabel('Sub Total', self.frameSubTotal)
        self.subTotalName.setFixedSize(115,20)
        self.subTotalName.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: white;")
        self.subTotalName.setFont(self.H2)
        self.subTotalValueLabel = QLabel('S/ 0.00', self.frameSubTotal)
        self.subTotalValueLabel.setFixedSize(174,50)
        self.subTotalValueLabel.setStyleSheet("background-color: rgba(255, 255, 255, 180); color: black; border-radius: 10px;")
        self.subTotalValueLabel.setFont(self.H3)
        self.subTotalValueLabel.setAlignment(Qt.AlignCenter)

        self.frameSubTotalHC.addWidget(self.subTotalName)
        self.frameSubTotalHC.addWidget(self.subTotalValueLabel)


        ##########
        self.update_product_info(product_sku="", product_name="Producto no encontrado", product_isBulk=self.product_isBulk)
        ##########

        self.itemsProductVC.addWidget(self.framePeso)
        self.itemsProductVC.addWidget(self.framePrecio)
        self.itemsProductVC.addWidget(self.frameSubTotal)

        self.boxProductHC.addWidget(self.imageBoxProduct)
        self.boxProductHC.addWidget(self.itemsProduct)

        # Add the bar frame to the detection panel layout
        self.frameDetectionPanelVC.addWidget(self.frameBar)
        self.frameDetectionPanelVC.addSpacing(31)
        self.frameDetectionPanelVC.addLayout(self.frameProductLabel)
        self.frameDetectionPanelVC.addSpacing(24)
        self.frameDetectionPanelVC.addWidget(self.boxProduct)

        # Work Panel
        self.frameWorkPanel = QLabel(self.mainFrame)
        self.frameWorkPanelVC = QVBoxLayout(self.frameWorkPanel)
        self.frameWorkPanelVC.setContentsMargins(0, 0, 0, 0)

        self.listProductWidget = ShoppingCart()
        self.listProductWidget.setFixedSize(600,396)

        # Botones
        self.frameBotones = QLabel(self.frameWorkPanel)
        self.frameBotones.setFixedSize(600,124)
        self.frameBotones.setStyleSheet("background-color: #E1E1E1;")

        self.frameBotonesHC = QHBoxLayout(self.frameBotones)
        self.frameBotonesHC.setContentsMargins(0, 0, 0, 0)


        self.botonregistrarVenta = QPushButton("Registrar Venta", self.frameBotones)
        self.botonregistrarVenta.setFixedSize(360,64)
        self.botonregistrarVenta.setFont(self.H2)
        self.botonregistrarVenta.setFlat(True)
        self.botonregistrarVenta.setStyleSheet("background-color: #639C3B; color: white; border-radius: 15px;")
        
        self.frameBotonesHC.addWidget(self.botonregistrarVenta)

        self.frameWorkPanelVC.addWidget(self.listProductWidget)
        self.frameWorkPanelVC.addWidget(self.frameBotones)

        # Add detection panel to the main layout
        self.layoutVC.addWidget(self.frameDetectionPanel)
        self.layoutVC.addSpacing(31)
        self.layoutVC.addWidget(self.frameWorkPanel)

        # Teclado Numerico
        self.teclado_numerico = NumericKeyboard()
        self.teclado_numerico.setFixedSize(600, 566)
        self.teclado_numerico.numero_actualizado.connect(self.update_preciovalue)
        self.teclado_numerico.hide()

        self.teclado_numerico.botonSalir.clicked.connect(self.ocultar_teclado)
        self.teclado_numerico.botonAniadir.clicked.connect(self.addToCart_currProduct)

    def connect_to_database(self):
        try:
            connection = sqlite3.connect(self.db_path)
            print("Conexión a la base de datos exitosa.")
            return connection
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
        return None

    def mostrar_teclado(self, event):
        # Mostrar el widget del teclado numérico
        self.layoutVC.removeWidget(self.frameWorkPanel)
        self.frameWorkPanel.hide()
        self.layoutVC.addWidget(self.teclado_numerico)
        self.teclado_numerico.show()

        # Crear la animación
        self.animacion_teclado = QPropertyAnimation(self.teclado_numerico, b"geometry")
        self.animacion_teclado.setDuration(400)
        self.animacion_teclado.setStartValue(QRect(0, self.height(), self.teclado_numerico.width(), self.teclado_numerico.height()))
        self.animacion_teclado.setEndValue(QRect(0, self.height() - self.teclado_numerico.height(), self.teclado_numerico.width(), self.teclado_numerico.height()))

        # Iniciar la animación
        self.animacion_teclado.start()

    def ocultar_teclado(self):
        self.layoutVC.removeWidget(self.teclado_numerico)
        self.teclado_numerico.hide()
        self.layoutVC.addWidget(self.frameWorkPanel)
        self.frameWorkPanel.show()

    def update_preciovalue(self, numero):

        # Actualizar el texto del QLabel en tiempo real
        if not numero:
            formatted_value = "0.00"
        else:
            value = int(numero)
            # Formatear el valor con dos decimales
            formatted_value = f"{value // 100}.{value % 100:02}"

        self.product_price =  float(formatted_value)
        self.precioValue.setText("S/ " + formatted_value)

        self.update_subTotal()
        

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Deletes the widget
            else:
                layout.removeItem(item)  # For non-widget items like spacers
    
    def barcode_scanned(self, scanned_sku):
        product_info = self.get_product_by_sku(scanned_sku)
        print(product_info)
        if product_info:
            self.update_product_info(
                product_sku=product_info[0],
                product_name=product_info[1],
                product_isBulk=False,
                product_img_path=product_info[2]
            )
        else:
            self.update_product_info(product_sku="", product_name="Producto no encontrado")

    def get_product_by_sku(self, sku):
        if not self.connection:
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT sku, nombre_producto, path_image
                FROM tb_catalogo_productos
                WHERE sku = ?
            """, (sku,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al buscar el producto: {e}")
            return None
            
    def update_product_info(self, product_sku, product_name, product_isBulk=False, product_img_path=""):
        self.product_sku = product_sku
        self.product_name = str(product_name)[:40]
        self.product_img_path = product_img_path
        self.product_isBulk = product_isBulk
        self.product_quantity = 1
        self.product_weight = 0.0
        self.product_price = 0.0

        self.clear_layout(self.framePesoHC)

        self.productName.setText("  " +self.product_name)

        if self.product_name == "Producto no encontrado":
            self.imageBoxProduct.setPixmap(QPixmap("backend/database/product_images/NO-FOUND.png"))
            self.imageBoxProduct.setFixedSize(210, 220)

        if self.product_img_path:
            pixmap = QPixmap(self.product_img_path)
            scaled_pixmap = pixmap.scaled(210, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
            self.imageBoxProduct.setPixmap(scaled_pixmap)
            self.imageBoxProduct.setFixedSize(210, 220)
                                   
        if self.product_isBulk:
            self.pesoName = QLabel('Peso', self.framePeso)
        else:
            self.pesoName = QLabel('Cantidad', self.framePeso)

        self.pesoName.setFixedSize(115,20)
        self.pesoName.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: white;")
        self.pesoName.setFont(self.H2)
        self.framePesoHC.addWidget(self.pesoName)

        if self.product_isBulk:
            self.pesoValue = QLabel(f"{self.product_weight:.2f} Kg" , self.framePeso)
            self.pesoValue.setFixedSize(174,45)
            self.pesoValue.setStyleSheet("margin: 0px;"
                                        "background-color: rgba(255, 255, 255, 180);" 
                                        "color: black; border-radius: 10px;")
            self.pesoValue.setFont(self.H3)
            self.pesoValue.setAlignment(Qt.AlignCenter)
            self.framePesoHC.addWidget(self.pesoValue)
            self.precioName.setText("Precio x Kg")
        else:
            
            self.btn_decrease = QPushButton('-',self.framePeso)
            self.btn_decrease.setStyleSheet("QPushButton { "
                                            "margin: 0px;"
                                            "border: none; "  # Establecer el color del contorno
                                            "border-radius: 10px; "     # Bordes redondeados
                                            "background-color: #FFCA44; "  # Color de fondo 
                                            "color: #333333; "            # Color del texto
                                            "font-weight: bold; "
                                            "font-size: 18px;"
                                            "} ")
            self.btn_decrease.clicked.connect(self.decrease_quantity)
            self.btn_decrease.setFixedSize(45, 45)
            self.framePesoHC.addWidget(self.btn_decrease)

            self.pesoValue = QLabel(str(self.product_quantity), self.framePeso)
            self.pesoValue.setFixedSize(65,45)
            self.pesoValue.setStyleSheet("margin: 0px;"
                                        "background-color: rgba(255, 255, 255, 180);" 
                                        "color: black; border-radius: 10px;")
            self.pesoValue.setFont(self.H3)
            self.pesoValue.setAlignment(Qt.AlignCenter)
            self.framePesoHC.addWidget(self.pesoValue)

            # Botón para aumentar cantidad
            self.btn_increase = QPushButton('+',self.framePeso)
            self.btn_increase.setStyleSheet("QPushButton { "
                                            "margin: 0px;"
                                            "border: none; "  # Establecer el color del contorno
                                            "border-radius: 10px; "     # Bordes redondeados
                                            "background-color: #FFCA44; "  # Color de fondo
                                            "color: #333333; "            # Color del texto
                                            "font-weight: bold; "
                                            "font-size: 18px;"
                                            "} ")

            self.btn_increase.setFixedSize(45, 45)
            self.btn_increase.clicked.connect(self.increase_quantity)
            self.framePesoHC.addWidget(self.btn_increase)
            self.precioName.setText("Precio")

            self.update_preciovalue(self.product_price)
        
    def decrease_quantity(self):
        if self.product_quantity > 1:
            self.product_quantity = self.product_quantity - 1  
        
        self.pesoValue.setText(str(self.product_quantity))
    
    def increase_quantity(self):
        self.product_quantity += 1 
        self.pesoValue.setText(str(self.product_quantity))

    def update_weight(self, weight):
        self.product_weight = weight
        self.update_subTotal()

    def update_subTotal(self):
        subtotal_value_str = ""
        if self.product_isBulk:
            subtotal_value_str = f"S/ {self.product_price*self.product_weight:.2f}"
        else:
            subtotal_value_str = f"S/ {self.product_price*self.product_quantity:.2f}"

        self.subTotalValueLabel.setText(subtotal_value_str)
    
    def addToCart_currProduct(self):
        self.teclado_numerico.numeros_presionados.clear

        if self.product_name == "Producto no encontrado":
            return
        
        if self.product_isBulk:
            self.listProductWidget.add_product(self.product_sku, self.product_name, self.product_price, self.product_quantity)
        else:
            self.listProductWidget.add_product(self.product_sku, self.product_name, self.product_price, self.product_quantity, self.product_weight, self.product_isBulk)

        product_sku = ""
        product_name = ""
        product_isBulk = False
        product_img_path = ""
        self.update_product_info(product_sku, product_name, product_isBulk, product_img_path)
        self.product_price = 0.0
        self.listProductWidget.get_products_list()
        self.teclado_numerico.reset_keyboard()
        self.ocultar_teclado()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.rbTimeBar.setText(now)  
        QTimer.singleShot(1000, self.update_clock)

    def verDashboard(self):
        self.dashboard = ReportMethod(self)  # Pasar self si necesita el padre
        self.dashboard.show()

    def reset_product_info(self):
        self.update_product_info("", "Producto no encontrado", False, "backend/database/product_images/NO-FOUND.png")
        self.listProductWidget.reset_cart()
