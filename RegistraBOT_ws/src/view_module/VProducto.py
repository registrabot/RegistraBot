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

class VProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        ## ======================================================
        ##              PRODUCT DETECTION WINDOW
        ## =====================================================
        # HC  : Horizontal Container
        # VC  : Vertical Container
        # wgt : Widget

        self.setWindowTitle("Ventana Producto")
        self.setFixedSize(480, 320)
        self.setStyleSheet("background-color: white;")

        # Central widget
        self.central_wgt = QLabel(self)
        self.central_wgt.setGeometry(10,10,460,300)
        self.layoutVC = QVBoxLayout(self.central_wgt)
        self.layoutVC.setSpacing(14)
        self.layoutVC.setContentsMargins(0, 0, 0, 0)

        # Font - Style
        self.H1 = QFont("Tahoma", 21)
        self.H2 = QFont("Tahoma", 12, QFont.Bold)
        self.H3 = QFont("Tahoma", 11)
        self.H4 = QFont("Tahoma", 9)
        self.H5 = QFont("Tahoma", 19, QFont.Bold)
        self.H6 = QFont("Tahoma", 14)
        self.H7 = QFont("Tahoma", 16, QFont.Bold)

        ## =================================================
        ##              NAVBAR BLOCK
        ## =================================================
        # HC  : Horizontal Container
        # VC  : Vertical Container
        # wgt : Widget

        # Navigation Bar
        self._navBar_wgt = QLabel(self.central_wgt)
        self._navBar_wgt.setFixedHeight(45)
        self._navBar_wgt.setStyleSheet("background-color: #FF8811; border-radius: 10px;")
        self._navBarHC = QHBoxLayout(self._navBar_wgt)
        self._navBarHC.setContentsMargins(15, 0, 15, 0)

        # Date Label
        self._date = datetime.now()
        self._formatted_date = self._date.strftime("%d/%m/%Y")
        self._dateLabel = QLabel(self._formatted_date, self._navBar_wgt)
        self._dateLabel.setFont(self.H6)
        self._dateLabel.setStyleSheet("background-color: #FF8811; color: white;")
        self._dateLabel.setFixedSize(120, 45)

        # Time Label
        self._time = QLabel('', self._navBar_wgt)
        self._time.setFont(self.H6)
        self._time.setStyleSheet("background-color: #FF8811; color: white;")
        self._time.setFixedSize(120, 45)
        self.update_clock()

        # Box: Car - List - Item
        self._carListItem_wgt = QLabel(self._navBar_wgt)
        self._carListItemHC = QHBoxLayout(self._carListItem_wgt)
        self._carListItemHC.setContentsMargins(0, 0, 0, 0)

        # CarShop Image
        self._carShopImage = QPixmap('view_module/images/Cart.png')
        self._carShop = QLabel(self._carListItem_wgt)
        self._carShop.setPixmap(self._carShopImage)
        self._carShop.setStyleSheet("background-color: #FF8811;")

        # List Label
        self._buyList = QLabel('Lista de Compra:', self._carListItem_wgt)
        self._buyList.setFont(self.H6)
        self._buyList.setStyleSheet("background-color: #FF8811; color: white;")

        # Item Label
        self._item = QLabel(self._carListItem_wgt)
        self._item.setFixedSize(30, 30)
        self._item.setStyleSheet("background-color: white; border-radius: 15px;")

        # Add Widget in Car - List - Item Box
        self._carListItemHC.addWidget(self._carShop)
        self._carListItemHC.addWidget(self._buyList)
        self._carListItemHC.addWidget(self._item)

        # Add Widget in NavBar Box
        self._navBarHC.addWidget(self._dateLabel)
        self._navBarHC.addWidget(self._time)
        self._navBarHC.addWidget(self._carListItem_wgt)

        # Add Widget in VerticalLayout
        self.layoutVC.addWidget(self._navBar_wgt)

        ## =================================================
        ##      PRODUCT DETECTION AND LABELS BLOCK
        ## =================================================
        # HC  : Horizontal Container
        # VC  : Vertical Container
        # wgt : Widget
        
        # Labels Box
        self._labelsBlock_wgt = QLabel(self.central_wgt)
        self._labelsBlockVC = QVBoxLayout(self._labelsBlock_wgt)
        self._labelsBlockVC.setSpacing(15)
        self._labelsBlockVC.setContentsMargins(0, 0, 0, 0)

        # Product Name Label
        self._productNameLabel_wgt = QLabel('Entre 3 productos ...', self._labelsBlock_wgt)
        self._productNameLabel_wgt.setStyleSheet("background-color: #F3F3F3; border-radius: 10px; padding: 10px; color: #6C6C6C;")

        # Weight Box
        self._weightBlock_wgt = QLabel(self._labelsBlock_wgt)
        self._weightBlockHC = QHBoxLayout(self._weightBlock_wgt)
        self._weightBlockHC.setSpacing(20)
        self._weightBlockHC.setContentsMargins(0, 0, 0, 0)

        self._weightLabel = QLabel('Peso (Kg)',self._weightBlock_wgt)
        self._weightLabel.setStyleSheet("background-color: white; border-radius: 10px; color: #6C6C6C;")

        self._weightDataInput = QLabel('0.00',self._weightBlock_wgt)
        self._weightDataInput.setAlignment(Qt.AlignCenter)
        self._weightDataInput.setStyleSheet("background-color: #F3F3F3; border-radius: 10px; color: #6C6C6C; padding: 10px;")

        # Add widget in Weight Box
        self._weightBlockHC.addWidget(self._weightLabel)
        self._weightBlockHC.addWidget(self._weightDataInput)

        # Price x weight Box
        self._priceWeightBlock_wgt = QLabel(self._labelsBlock_wgt)
        self._priceWeightBlockHC = QHBoxLayout(self._priceWeightBlock_wgt)
        self._priceWeightBlockHC.setSpacing(20)
        self._priceWeightBlockHC.setContentsMargins(0, 0, 0, 0)

        self._priceWeightLabel = QLabel('Precio x Kg',self._priceWeightBlock_wgt)
        self._priceWeightLabel.setStyleSheet("background-color: white; border-radius: 10px; color: #6C6C6C;")

        self._priceWeightDataInput = QLabel('0.00',self._priceWeightBlock_wgt)
        self._priceWeightDataInput.setAlignment(Qt.AlignCenter)
        self._priceWeightDataInput.setStyleSheet("background-color: #F3F3F3; border-radius: 10px; color: #6C6C6C; padding: 10px;")

        # Add widget in Price x weight Box
        self._priceWeightBlockHC.addWidget(self._priceWeightLabel)
        self._priceWeightBlockHC.addWidget(self._priceWeightDataInput)

        # Total Price Box
        self._totalPriceBlock_wgt = QLabel(self._labelsBlock_wgt)
        self._totalPriceHC = QHBoxLayout(self._totalPriceBlock_wgt)
        self._totalPriceHC.setSpacing(20)
        self._totalPriceHC.setContentsMargins(0, 0, 0, 0)

        self._totalPriceLabel = QLabel('Total (S/.)',self._totalPriceBlock_wgt)
        self._totalPriceLabel.setStyleSheet("background-color: white; border-radius: 10px; color: #6C6C6C;")

        self._totalPriceDataInput = QLabel('0.00',self._totalPriceBlock_wgt)
        self._totalPriceDataInput.setAlignment(Qt.AlignCenter)
        self._totalPriceDataInput.setStyleSheet("background-color: #F3F3F3; border-radius: 10px; color: #6C6C6C; padding: 10px;")

        # Add widget in Total Price Box
        self._totalPriceHC.addWidget(self._totalPriceLabel)
        self._totalPriceHC.addWidget(self._totalPriceDataInput)

        # Add Widget in Labels Box
        self._labelsBlockVC.addWidget(self._productNameLabel_wgt)
        self._labelsBlockVC.addWidget(self._weightBlock_wgt)
        self._labelsBlockVC.addWidget(self._priceWeightBlock_wgt)
        self._labelsBlockVC.addWidget(self._totalPriceBlock_wgt)

        # Product Detection Box
        self._productdetectionBlock_wgt = ResizeImage(self.central_wgt)
        self._productdetectionBlock_wgt.setRoundedPixmap(QPixmap('view_module/images/cocacola_lata.png'), 100)
        self._productdetectionBlock_wgt.setStyleSheet("background-color: #F3F3F3;")

        # Product and Label Box
        self._productLabel_wgt = QLabel(self.central_wgt)
        self._productLabelHC = QHBoxLayout(self._productLabel_wgt)
        self._productLabelHC.setSpacing(22)
        self._productLabelHC.setContentsMargins(0, 0, 0, 0)
        
        # Add widget in Product Label Horizontal Layout
        self._productLabelHC.addWidget(self._productdetectionBlock_wgt)
        self._productLabelHC.addWidget(self._labelsBlock_wgt)

        # Add widget in Product Label Vertical Layout
        self.layoutVC.addWidget(self._productLabel_wgt)
    
    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self._time.setText(now)
        QTimer.singleShot(1000, self.update_clock)