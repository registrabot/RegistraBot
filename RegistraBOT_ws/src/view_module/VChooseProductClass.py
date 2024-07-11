## VChooseProduct.py

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

class ResizeImage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.p = QPixmap()

    def setPixmap(self, p):
        self.p = p
        self.update()

    def setRoundedPixmap(self, pixmap, radius):
        size = pixmap.size()
        rounded = QPixmap(size)
        rounded.fill(Qt.transparent)

        # Use QPainter to draw the rounded pixmap
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(0, 0, size.width(), size.height())
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.setPixmap(rounded)

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)


class VElegirProducto(QMainWindow):
    def __init__(self, productos_info=None):
        super().__init__()
        self.setup_ui()
        self.create_navbar()

        if productos_info is not None:
            self.create_product_block(productos_info)
        else:
            print("No se han proporcionado productos_info.")

        self.update_clock()

    def setup_ui(self):
        self.setWindowTitle("Ventana Elegir Producto")
        self.setFixedSize(480, 320)
        self.setStyleSheet("background-color: white;")

        self.central_wgt = QLabel(self)
        self.central_wgt.setGeometry(10, 10, 460, 300)
        self.layoutVC = QVBoxLayout(self.central_wgt)
        self.layoutVC.setSpacing(14)
        self.layoutVC.setContentsMargins(0, 0, 0, 0)

        self.H1 = QFont("Tahoma", 21)
        self.H2 = QFont("Tahoma", 12, QFont.Bold)
        self.H3 = QFont("Tahoma", 11)
        self.H4 = QFont("Tahoma", 9)
        self.H5 = QFont("Tahoma", 19, QFont.Bold)
        self.H6 = QFont("Tahoma", 14)
        self.H7 = QFont("Tahoma", 16, QFont.Bold)

    def create_navbar(self):
        self._navBar_wgt = QLabel(self.central_wgt)
        self._navBar_wgt.setFixedHeight(45)
        self._navBar_wgt.setStyleSheet("background-color: #FF8811; border-radius: 10px;")
        self._navBarHC = QHBoxLayout(self._navBar_wgt)
        self._navBarHC.setContentsMargins(15, 0, 15, 0)

        self._date = datetime.now()
        self._formatted_date = self._date.strftime("%d/%m/%Y")
        self._dateLabel = QLabel(self._formatted_date, self._navBar_wgt)
        self._dateLabel.setFont(self.H6)
        self._dateLabel.setStyleSheet("background-color: #FF8811; color: white;")
        self._dateLabel.setFixedSize(120, 45)

        self._time = QLabel('', self._navBar_wgt)
        self._time.setFont(self.H6)
        self._time.setStyleSheet("background-color: #FF8811; color: white;")
        self._time.setFixedSize(120, 45)

        self._carListItem_wgt = QLabel(self._navBar_wgt)
        self._carListItemHC = QHBoxLayout(self._carListItem_wgt)
        self._carListItemHC.setContentsMargins(0, 0, 0, 0)
        
        self._carShop = QLabel(self._carListItem_wgt)
        car_shop_image_path = 'view_module/images/Cart.png'
        if os.path.exists(car_shop_image_path):
            self._carShopImage = QPixmap(car_shop_image_path)
            self._carShop.setPixmap(self._carShopImage)
            self._carShop.setStyleSheet("background-color: #FF8811;")
        else:
            print(f"Image not found: {car_shop_image_path}")

        self._buyList = QLabel('Lista de Compra:', self._carListItem_wgt)
        self._buyList.setFont(self.H6)
        self._buyList.setStyleSheet("background-color: #FF8811; color: white;")

        self._item = QLabel(self._carListItem_wgt)
        self._item.setFixedSize(30, 30)
        self._item.setStyleSheet("background-color: white; border-radius: 15px;")

        self._carListItemHC.addWidget(self._carShop)
        self._carListItemHC.addWidget(self._buyList)
        self._carListItemHC.addWidget(self._item)

        self._navBarHC.addWidget(self._dateLabel)
        self._navBarHC.addWidget(self._time)
        self._navBarHC.addWidget(self._carListItem_wgt)

        self.layoutVC.addWidget(self._navBar_wgt)

    def create_product_block(self, productos_info):
        self._productsBlock_wgt = QLabel(self.central_wgt)
        self._productsBlock_wgt.setFixedHeight(226)
        self._productsBlockHC = QHBoxLayout(self._productsBlock_wgt)
        self._productsBlockHC.setSpacing(20)
        self._productsBlockHC.setContentsMargins(0, 0, 0, 0)

        product_info = []
        select_option = 1

        for index, row in productos_info.iterrows():
            image_path = row['path_image']  # Ruta de la imagen desde los datos
            label_num = f"{select_option}:"     # Número de etiqueta, por ejemplo '1:', '2:', etc.
            label_text = row['nombre_producto']  # Nombre del producto desde los datos
            select_option +=1
        
            product_info.append({
                'image_path': image_path,
                'label_num': label_num,
                'label_text': label_text
            })

        print(product_info)
        for info in product_info:
            self.create_product(self._productsBlockHC, info['image_path'], info['label_num'], info['label_text'])

        self.layoutVC.addWidget(self._productsBlock_wgt)

    def create_product(self, parent_layout, image_path, label_num, label_text):
        product_block_wgt = QLabel(self._productsBlock_wgt)
        product_block_VC = QVBoxLayout(product_block_wgt)
        product_block_VC.setSpacing(22)
        product_block_VC.setContentsMargins(0, 0, 0, 0)

        product_image_wgt = ResizeImage(product_block_wgt)
        product_image_wgt.setFixedHeight(159)
        if os.path.exists(image_path):
            product_image_wgt.setRoundedPixmap(QPixmap(image_path), 70)
        else:
            print(f"Image not found: {image_path}")

        product_label_wgt = QLabel(product_block_wgt)
        product_label_wgt.setStyleSheet("background-color: #F3F3F3; border-radius: 10px; color: #6C6C6C;")
        product_label_HC = QHBoxLayout(product_label_wgt)
        product_label_HC.setContentsMargins(0, 0, 0, 0)
        product_label_HC.setSpacing(0)

        product_label_num_wgt = QLabel(label_num, product_label_wgt)
        product_label_num_wgt.setFixedWidth(40)
        product_label_num_wgt.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        product_label_num_wgt.setStyleSheet("background-color: #F3F3F3; color: #FF8811;")
        
        product_label_text_wgt = QLabel(label_text, product_label_wgt)
        product_label_text_wgt.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        product_label_text_wgt.setStyleSheet("background-color: #F3F3F3; color: #6C6C6C; padding: 5px;")

        product_label_HC.addWidget(product_label_num_wgt)
        product_label_HC.addWidget(product_label_text_wgt)

        product_block_VC.addWidget(product_image_wgt)
        product_block_VC.addWidget(product_label_wgt)

        parent_layout.addWidget(product_block_wgt)

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self._time.setText(now)
        QTimer.singleShot(1000, self.update_clock)