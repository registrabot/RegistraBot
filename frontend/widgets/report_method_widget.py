import sys
import signal
import calendar
import sqlite3
from datetime import date
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ReportMethod(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ventana Reporte Bodeguero")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(556, 932)
        self.setModal(True)

        self.current_month = QDate.currentDate().month()
        self.current_year = QDate.currentDate().year()

        self.db_path = '/home/pato/RegistraBot/backend/database/BD_RegistraBOT.db'
        self.connection = self.connect_to_database()

        # Bordes Redondos
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Widget principal con bordes redondeados
        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(0, 0, 556, 932)
        self.mainWidget.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 20px; color: black;")
        #self.mainWidget.setStyleSheet("background-color: white; border-radius: 20px; color: black;")

        # Font Styles
        self.H1 = QFont("Tahoma", 21)
        self.H2 = QFont("Tahoma", 12, QFont.Bold)
        self.H3 = QFont("Tahoma", 11, QFont.Bold)
        self.H4 = QFont("Tahoma", 14)
        self.H5 = QFont("Tahoma", 19, QFont.Bold)
        self.H6 = QFont("Tahoma", 10)
        self.H7 = QFont("Tahoma", 16, QFont.Bold)
        self.H8 = QFont("Tahoma", 14, QFont.Bold)
        self.H9 = QFont("Tahoma", 16)

        # Frame Center
        self.mainFrame = QLabel(self.mainWidget)
        self.mainFrame.setGeometry(0, 0, 556, 932)
        #self.mainFrame.setStyleSheet("background-color:rgba(255, 255, 255, 0.8); border: 2px solid black;")
        self.mainFrame.setStyleSheet("background-color:rgba(255, 255, 255); border: 2px solid black;")
        self.layoutVC = QVBoxLayout(self.mainFrame)
        self.layoutVC.setContentsMargins(0, 0, 0, 0)

        # Text
        self.textLabel = QLabel('Reporte de Ventas', self.mainFrame)
        self.textLabel.setGeometry(0, 0, 502, 44)
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setFont(self.H5)
        self.textLabel.setStyleSheet("background-color: #FDA22A; border: none; color: white")

        self.botonBackHome = QPushButton('Regresar', self.mainFrame)
        self.botonBackHome.setGeometry(15, 15, 120, 40)
        self.botonBackHome.setFont(self.H2)
        self.botonBackHome.setFlat(True)
        self.botonBackHome.setStyleSheet("background-color: #639C3B; color: white; border: none; border-radius: none;")

        self.botonBackHome.clicked.connect(self.close)

        # Date Filters
        self.dateLabel = QWidget(self.mainFrame)
        self.dateLabel.setFixedHeight(70)
        self.dateLabel.setStyleSheet("background-color: rgba(255, 255, 255, 0); border: none;")

        # Month
        self.monthWidget = QWidget(self.mainFrame)
        self.monthWidget.setStyleSheet("color: white; background-color: #639C3B; border-radius: 10px; border: none; font-weight: bold;")
        self.monthWidgetHC = QHBoxLayout(self.monthWidget)

        self.monthLeftButton = QPushButton("◀", self.monthWidget)
        self.monthLeftButton.setStyleSheet("border: none; background: transparent;")
        self.monthLeftButton.setFont(self.H1)
        self.monthLeftButton.clicked.connect(self.on_month_left_button_pressed)

        self.monthRightButton = QPushButton("▶", self.monthWidget)
        self.monthRightButton.setStyleSheet("border: none; background: transparent;")
        self.monthRightButton.setFont(self.H1)
        self.monthRightButton.clicked.connect(self.on_month_right_button_pressed)

        self.monthLabel = QLabel()
        self.monthLabel.setStyleSheet("border: none; background: transparent;")
        self.monthLabel.setFont(self.H4)
        self.monthLabel.setAlignment(Qt.AlignCenter)
        self.monthLabel.setText(self.get_month_in_spanish())

        self.monthWidgetHC.addWidget(self.monthLeftButton)
        self.monthWidgetHC.addWidget(self.monthLabel)
        self.monthWidgetHC.addWidget(self.monthRightButton)

        # Year
        self.yearWidget = QWidget(self.mainFrame)
        self.yearWidget.setStyleSheet("color: white; background-color: #639C3B; border-radius: 10px; border: none; font-weight: bold;")
        self.yearWidgetHC = QHBoxLayout(self.yearWidget)

        self.yearLeftButton = QPushButton("◀")
        self.yearLeftButton.setFont(self.H1)
        self.yearLeftButton.clicked.connect(self.on_year_left_button_pressed)

        self.yearRightButton = QPushButton("▶")
        self.yearRightButton.setFont(self.H1)
        self.yearRightButton.clicked.connect(self.on_year_right_button_pressed)

        self.yearLabel = QLabel()
        self.yearLabel.setFont(self.H4)
        self.yearLabel.setAlignment(Qt.AlignCenter)
        self.yearLabel.setText("")

        self.yearWidgetHC.addWidget(self.yearLeftButton)
        self.yearWidgetHC.addWidget(self.yearLabel)
        self.yearWidgetHC.addWidget(self.yearRightButton)

        self.dateSelectors_layout = QHBoxLayout(self.dateLabel)
        self.dateSelectors_layout.addWidget(self.monthWidget)
        self.dateSelectors_layout.addWidget(self.yearWidget)

         # Indicadores
        self.total_sales_label = QLabel(self.mainFrame)
        self.total_sales_label.setStyleSheet("border: none;")
        self.total_salesHC = QHBoxLayout(self.total_sales_label)

        self.total_sales_text = QLabel("Total Ventas: ", self.total_sales_label)
        self.total_sales_text.setStyleSheet("background-color: none; border: none")
        self.total_sales_text.setFont(self.H8)
        self.total_sales_text.setAlignment(Qt.AlignCenter)

        self.total_sales_num = QLabel("0.00", self.total_sales_label)
        self.total_sales_num.setFixedHeight(65)
        self.total_sales_num.setStyleSheet("color: black; font-weight: bold; border: 2px solid #FDA22A;")
        self.total_sales_num.setAlignment(Qt.AlignCenter)
        self.total_sales_num.setFont(self.H9)

        self.total_salesHC.addWidget(self.total_sales_text)
        self.total_salesHC.addWidget(self.total_sales_num)

        self.count_sales_label = QLabel(self.mainFrame)
        self.count_sales_label.setStyleSheet("border: none;")
        self.count_salesHC = QHBoxLayout(self.count_sales_label)

        self.count_sales_text = QLabel("Cantidad Ventas: ", self.count_sales_label)
        self.count_sales_text.setStyleSheet("background-color: none;")
        self.count_sales_text.setFont(self.H8)
        self.count_sales_text.setAlignment(Qt.AlignCenter)

        self.count_sales_num = QLabel("0.00", self.count_sales_label)
        self.count_sales_num.setFixedHeight(65)
        #self.count_sales_num.setStyleSheet("background-color: #FDA22A; color: white; font-weight: bold;")
        self.count_sales_num.setStyleSheet("color: black; font-weight: bold; border: 2px solid #FDA22A;")
        self.count_sales_num.setAlignment(Qt.AlignCenter)
        self.count_sales_num.setFont(self.H9)

        self.count_salesHC.addWidget(self.count_sales_text)
        self.count_salesHC.addWidget(self.count_sales_num)

        self.top_products_label = QLabel(self.mainFrame)
        self.top_products_label.setStyleSheet("border: none;")
        self.top_productsHC = QHBoxLayout(self.top_products_label)

        self.top_products_text = QLabel("Top 5 Productos: ", self.top_products_label)
        self.top_products_text.setStyleSheet("background-color: none;")
        self.top_products_text.setFont(self.H8)
        self.top_products_text.setAlignment(Qt.AlignCenter)

        self.top_products_num = QLabel("", self.top_products_label)
        #self.top_products_num.setStyleSheet("background-color: #FDA22A; color: white; font-weight: bold;")
        self.top_products_num.setStyleSheet("color: black; font-weight: bold; border: 2px solid #FDA22A;")
        self.top_products_num.setAlignment(Qt.AlignCenter)
        self.top_products_num.setFont(self.H4)

        self.top_productsHC.addWidget(self.top_products_text)
        self.top_productsHC.addWidget(self.top_products_num)
        
        # Agregar Widgets 
        self.layoutVC.addWidget(self.textLabel)
        self.layoutVC.addWidget(self.dateLabel)
        self.layoutVC.addWidget(self.total_sales_label)
        self.layoutVC.addWidget(self.count_sales_label)
        self.layoutVC.addWidget(self.top_products_label)

        # Posicionar la ventana al centro
        self.center_dialog()
        self.update_date_labels()

    def connect_to_database(self):
        try:
            connection = sqlite3.connect(self.db_path)
            print("Conexión a la base de datos exitosa.")
            return connection
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
        return None
    
    def on_month_left_button_pressed(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_date_labels()

    def on_month_right_button_pressed(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_date_labels()

    def update_date_labels(self):
        self.monthLabel.setText(self.get_month_in_spanish())
        self.yearLabel.setText(str(self.current_year))
        start_date, end_date = self.get_start_and_end_dates(self.current_month, self.current_year)
        self.update_indicators(start_date, end_date)
        print(f"Start date: {start_date}, End date: {end_date}")

    def get_month_in_spanish(self):
        locale = QLocale(QLocale.Spanish, QLocale.Spain)
        month = locale.toString(QDate(self.current_year, self.current_month, 1), "MMMM")
        return month.capitalize()
    
    def on_year_left_button_pressed(self):
        self.current_year -= 1
        self.yearLabel.setText(str(self.current_year))
        self.update_date_labels()
    
    def on_year_right_button_pressed(self):
        self.current_year += 1
        self.yearLabel.setText(str(self.current_year))
        self.update_date_labels()
    
    def get_start_and_end_dates(self, month: int, year: int):
        start_date = f"{year}-{month:02d}-01"
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}-{month:02d}-{last_day}"
        return start_date, end_date
    
    def update_indicators(self, start_date, end_date):
        cursor = self.connection.cursor()

        # Total de ventas
        cursor.execute("""
            SELECT SUM(precio_total) FROM tb_registro_ventas
            WHERE DATE(insert_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        total_sales = cursor.fetchone()[0] or 0
        print(f"Total Ventas: {total_sales}")
        self.total_sales_num.setText(f"S/. {total_sales:.2f}")

        # Cantidad de ventas
        cursor.execute("""
            SELECT COUNT(DISTINCT id_venta) FROM tb_registro_ventas
            WHERE DATE(insert_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        count_sales = cursor.fetchone()[0] or 0
        self.count_sales_num.setText(str(count_sales))

        # Top 5 productos más vendidos
        cursor.execute("""
            SELECT
                cp.nombre_producto, 
                SUM(rv.cantidad) AS total_cantidad 
            FROM tb_registro_ventas rv
            JOIN tb_catalogo_productos cp ON rv.sku = cp.sku
            WHERE DATE(rv.insert_date) BETWEEN ? AND ?
            GROUP BY cp.nombre_producto
            ORDER BY total_cantidad DESC
            LIMIT 5
        """, (start_date, end_date))
        top_products = cursor.fetchall()

        top_products_text = "\n".join([f"{idx+1}. {nombre_producto[:15]}: {cantidad}" for idx, (nombre_producto, cantidad) in enumerate(top_products)])
        self.top_products_num.setText(top_products_text)
        
        cursor.close()

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