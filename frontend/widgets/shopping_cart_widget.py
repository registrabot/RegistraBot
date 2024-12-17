import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,QFrame,  QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
class ProductWidget(QWidget):
    def __init__(self, name, unit_price, update_total_callback, quantity=1, weight=0, is_bulk=False):
        super().__init__()
        self.name = name
        self.unit_price = unit_price
        self.is_bulk = is_bulk
        self.quantity = quantity if not is_bulk else 0  # 0 para productos a granel
        self.weight = weight  # Peso inicial para productos a granel
        self.update_total_callback = update_total_callback  # Callback para actualizar el total
        self.init_ui()

    def init_ui(self):

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # Layout horizontal para cada producto
        container = QFrame(self)
        container.setStyleSheet("background-color: white; border-radius: 10px;")
        
        layout = QHBoxLayout(container)

        # Nombre del producto
        self.name_label = QLabel(self.name, self)
        #self.name_label.setFixedWidth(120) 
        layout.addWidget(self.name_label)

        # Botón para reducir cantidad
        if not self.is_bulk:
            self.btn_decrease = QPushButton('-',self)
            self.btn_decrease.setStyleSheet("QPushButton { "
                             "border: none; "  # Establecer el color del contorno
                             "border-radius: 10px; "     # Bordes redondeados
                             "background-color: #DF4128; "  # Color de fondo
                             "color: white; "            # Color del texto
                             "} ")
            self.btn_decrease.clicked.connect(self.decrease_quantity)
            self.btn_decrease.setFixedSize(30, 30)
            layout.addWidget(self.btn_decrease)

            # Cantidad
            self.quantity_label = QLabel(str(self.quantity),self)
            self.quantity_label.setFixedWidth(34) 
            self.quantity_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.quantity_label)

            # Botón para aumentar cantidad
            self.btn_increase = QPushButton('+',self)
            self.btn_increase.setStyleSheet("QPushButton { "
                             "border: none; "  # Establecer el color del contorno
                             "border-radius: 10px; "     # Bordes redondeados
                             "background-color: gray; "  # Color de fondo
                             "color: white; "            # Color del texto
                             "} "
                             "QPushButton:hover { "
                             "background-color: green; "  # Color al pasar el ratón
                             "}")
            self.btn_increase.setFixedSize(30, 30)
            self.btn_increase.clicked.connect(self.increase_quantity)
            layout.addWidget(self.btn_increase)
            
            # Cantidad
            self.unit_price_label = QLabel(f"S/ {self.unit_price:.2f}",self)
            self.unit_price_label.setFixedWidth(100) 
            self.unit_price_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.unit_price_label)

            # Botón de eliminar
            self.btn_delete = QPushButton(self)
            pixmap = QPixmap("../Imagenes/tachito.png")
            self.btn_delete.setIcon(QIcon(pixmap))
            self.btn_delete.setIconSize(pixmap.size())  # Ajustar el tamaño del icono al tamaño original de la imagen
            #self.btn_delete.setFixedSize(pixmap.size())
            self.btn_delete.setFixedSize(40, 40)
            self.update_delete_button()
            self.btn_delete.clicked.connect(self.delete_product)
            layout.addWidget(self.btn_delete)

        # Peso o cantidad (solo para productos a granel)
        if self.is_bulk:
            self.weight_label = QLabel(f"{self.weight:.2f} Kg", self)
            self.weight_label.setFixedWidth(94) 
            self.weight_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.weight_label)

            # Botón de eliminar solo para productos a granel
            self.btn_delete_bulk = QPushButton( self)
            pixmap = QPixmap("../Imagenes/tachito.png")
            self.btn_delete_bulk.setIcon(QIcon(pixmap))
            self.btn_delete_bulk.setIconSize(pixmap.size())  # Ajustar el tamaño del icono al tamaño original de la imagen
            #self.btn_delete_bulk.setFixedSize(pixmap.size())  # Ajustar el tamaño del botón al tamaño de la imagen
            self.btn_delete_bulk.setFixedSize(40, 40)
            # Hacer que el botón sea solo la imagen, sin bordes ni fondo adicional
            self.btn_delete_bulk.setStyleSheet("border: none; background-color: transparent;")
            
            # price_per_Kg
            self.price_per_kg_label = QLabel(f"S/ {self.unit_price:.2f}",self)
            self.price_per_kg_label.setFixedWidth(100) 
            self.price_per_kg_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.price_per_kg_label)

            
            self.btn_delete_bulk.clicked.connect(self.delete_product)
            layout.addWidget(self.btn_delete_bulk)

        main_layout.addWidget(container)
        self.setLayout(main_layout)
        self.setFixedHeight(60)  # Altura fija del widget
        
    def increase_quantity(self):
        self.quantity += 1  # Aumenta la cantidad
        self.quantity_label.setText(str(self.quantity))
        self.update_delete_button()
        self.update_total_callback()

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.quantity_label.setText(str(self.quantity))
            self.update_delete_button()
        else:
            self.delete_product()  # Elimina el producto si la cantidad es 1
        self.update_total_callback()

    def update_delete_button(self):
        # Oculta el botón de eliminar si la cantidad es 1 o menor
        self.btn_delete.setEnabled(self.quantity > 1)

    def delete_product(self):
        self.setParent(None)  # Elimina el widget del carrito
        self.update_total_callback()

    def get_total_price(self):
        if self.is_bulk:
            return self.weight * self.unit_price
        else:
            return self.quantity * self.unit_price

class ShoppingCart(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carrito de Compras")
        #self.setFixedSize(520, 520)  # Tamaño fijo de la ventana
        self.cart_total_amount = 0
        # Layout principal
        main_layout = QVBoxLayout(self)

        # Crear el área de scroll
        scroll_area = QScrollArea(self)

        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;     /* Color de fondo del scroll bar */
                width: 12px;                   /* Ancho del scroll bar */
                margin: 15px 3px 15px 3px;     /* Márgenes para que no cubra todo el área */
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #a6a6a6;     /* Color de la "manija" o "handle" */
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #888888;     /* Color al pasar el mouse sobre la "manija" */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;              /* Eliminar los botones de arriba y abajo */
            }
        """)

        scroll_area.setWidgetResizable(True)

        # Contenedor para los productos
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)  # Layout de los productos
        #self.scroll_layout.setSpacing(10)  # Separación entre los elementos

        # Configurar el contenido dentro del área de scroll
        scroll_area.setWidget(self.scroll_content)

        # Crear layout para el total a pagar
        self.total_widget = QWidget()  # Envolver en un widget
        self.cart_total_amount_layout = QHBoxLayout(self.total_widget)

        font = QFont("Arial", 20)  # Font family and size

        self.total_label = QLabel("Total a pagar:")
        self.total_label.setFont(font)
        self.cart_total_amount_layout.addWidget(self.total_label)

        self.cart_total_amount_label = QLabel("S/"+ str(np.round(self.cart_total_amount,2)))
        self.cart_total_amount_label.setFont(font)
        self.cart_total_amount_label.setAlignment(Qt.AlignRight)
        self.cart_total_amount_layout.addWidget(self.cart_total_amount_label)


        # Agregar el área de scroll al layout principal
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.total_widget)

        # Agregar productos de ejemplo
        """self.add_product("Producto 1", 10.00)
        self.add_product("Producto 2", 15.50)
        self.add_product("Producto a Granel", 5.00, 1.33, is_bulk=True)
        self.add_product("Producto a Granel", 2.00, 1.9, is_bulk=True)
        self.add_product("Producto a Granel", 3.00, 5, is_bulk=True)"""

    def add_product(self, name, unit_price, quantity = 1, weight = 0, is_bulk=False):
        product_widget = ProductWidget(name, unit_price, self.update_total, quantity, weight, is_bulk)
        self.scroll_layout.addWidget(product_widget)
        self.update_total()

    def update_total(self):
        total = 0
        for i in range(self.scroll_layout.count()):
            product_widget = self.scroll_layout.itemAt(i).widget()
            total += product_widget.get_total_price()
        self.cart_total_amount_label.setText(f"S/ {total:.2f}")

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoppingCart()
    window.show()
    sys.exit(app.exec_())"""