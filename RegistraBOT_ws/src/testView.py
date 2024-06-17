from PyQt5.QtWidgets import QApplication
from viewProduct_weightsensor import VProducto


if __name__ == "__main__":
    app = QApplication([])
    ventana = VProducto()
    ventana.show()
    app.exec_()
