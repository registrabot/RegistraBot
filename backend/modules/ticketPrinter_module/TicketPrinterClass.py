import os
import sys
import time
from tabulate import tabulate
print('Original sys.path:', sys.path)
sys.path.append('/home/pato/rb_workspace/PrimerPrototipo/RegistraBOT_ws/src/ticketprinter_module/Python-Thermal-Printer')
print('Updated sys.path:', sys.path)
from Adafruit_Thermal import *

class TicketPrinter:
    def __init__(self):
        self.printer = Adafruit_Thermal("/dev/ttyS0", 9600, timeout=5)
        #self.printer = Adafruit_Thermal("/dev/usb/lp0", 9600, timeout=5)
        self.lista_productos = []
        self.precio_suma_total = 0.0
        self.metodo_pago = 'efectivo'
    def set_metodo_pago(self, metodo_pago):
        self.metodo_pago = metodo_pago

    def agregar_producto(self, nombre, cantidad, precio):
        # Limitar el nombre del producto a 20 caracteres
        #nombre_truncado = nombre[:9]
        self.lista_productos.append([nombre, cantidad, precio])
        self.precio_suma_total += cantidad * precio

    def truncar_palabras_intermedias(self, palabras, max_len=5):
        if len(palabras) <= 2:
            return palabras  # No hay palabras intermedias para truncar

        palabras_truncadas = [palabras[0]]  # Mantén las primeras dos palabras
        palabras_truncadas += [palabra[:max_len] for palabra in palabras[1:-1]]  # Trunca las intermedias
        palabras_truncadas.append(palabras[-1])  # Mantén la última palabra

        return palabras_truncadas

    def dividir_nombre_producto(self, nombre, ancho_maximo=20, max_palabra_len=3):
        palabras = nombre.split()
        palabras_truncadas = self.truncar_palabras_intermedias(palabras, max_len=max_palabra_len)
        nombre_truncado = ' '.join(palabras_truncadas)

        lineas = []
        while len(nombre_truncado) > ancho_maximo:
            espacio = nombre_truncado.rfind(' ', 0, ancho_maximo)
            if espacio == -1:
                espacio = ancho_maximo
            lineas.append(nombre_truncado[:espacio])
            nombre_truncado = nombre_truncado[espacio:].strip()
        lineas.append(nombre_truncado)
        return lineas

    def imprimir_ticket(self):
        ticket_text = ""
        ticket_text += "BODEGA JENNY\n"
        ticket_text += "dir.: Luis Galvez Chipoco 198 Alt cuadra 3 Brasil \n"
        ticket_text += "telef.: -\n"
        ticket_text += "RUC: -\n"
        ticket_text += "FECHA Y HORA: " + time.strftime("%x") + " " + time.strftime("%X") + "\n"
        ticket_text += "PRODUCTOS:\n"
        ticket_text += f"{'Producto':<19} {'Cant':>3} {'Precio':>7}\n"  # Encabezados
        for producto in self.lista_productos:
            nombre, cantidad, precio = producto
            lineas_nombre = self.dividir_nombre_producto(nombre)
            for i, linea in enumerate(lineas_nombre):
                if i == len(lineas_nombre) - 1:
                    # En la última línea, imprimir el nombre seguido por la cantidad y el precio
                    ticket_text += f"{linea:<19} {cantidad:>3} {precio:>7.2f}\n"
                else:
                    # Imprimir las líneas intermedias del nombre
                    ticket_text += f"{linea}\n"
        ticket_text += "\n"
        ticket_text += "TOTAL A PAGAR: " + str(self.precio_suma_total) + "\n"
        ticket_text += "METODO DE PAGO: " + (self.metodo_pago) + "\n"
        ticket_text += "GRACIAS POR TU COMPRA\n"
        
        # Imprimir en terminal para pruebas
        #print(ticket_text)
        
        # Imprimir en impresora física
        self.printer.println(ticket_text)
        self.printer.feed(3)  # Avanza 3 líneas para asegurarse de que el ticket se corte correctamente
