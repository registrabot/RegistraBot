import os
import argparse
import sys
import time
import threading
import importlib.util
import gspread
import pandas as pd

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from datetime import datetime
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import random
import re

import csv
import serial
import RPi.GPIO as GPIO



# ================================================================
#                DECLARACION DE VARIABLES GLOBALES
# ================================================================
       
id_producto = 0
lista_productos=[]
n_in_productos=0 
producto=["",""]
data = []

peso_producto = 0.000
peso_producto = format(peso_producto, '.3f')

precio_ref = 0
precio_unitario = 0

precio_total = 0.000
precio_total = format(precio_total,'.3f')

precio_suma_total = 0   
selector = 0
dataframe = []

identificador = None

# ==================
# PARAMETROS BUZZER
# ==================

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)

global Buzz
Buzz = GPIO.PWM(12,880)

# =========================
# PARAMETROS SENSOR DE PESO
# =========================

from hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup() 
    print("Bye!")
    sys.exit()

GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(21, GPIO.OUT)           # set GPIO24 as an output   
GPIO.output(21, 1)
hx = HX711(16, 20)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(-215)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# ===============================================================================
#  DECLARACION DE FUNCIONES Y PARAMETROS DEL MODELO DE RECONOCIMIENTO DE OBJETOS
# ===============================================================================

# Define and parse input arguments
parser = argparse.ArgumentParser()

parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5)
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='1280x720')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()
MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu

# IMPORTAMOS LIBRERIAS TENSORFLOW PARA RECONOCIMIENTO

pkg = importlib.util.find_spec('tflite_runtime')

if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate
   
# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map

labels_array = []
with open(PATH_TO_LABELS) as labels:
    for line in labels:
        x=line.split(", ")
        producto=x[0].split(" ",1)[1]
        marca=x[1].split("\n")[0]
        labels_array.append([producto, marca])
labels.close()

# CARGAMOS LA BASE DE DATOS
sa = gspread.service_account(filename="service_account.json")
sh = sa.open("registraBOTdata")
wks = sh.worksheet("data")

# CARGAMOS EL MODELO

if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()


# OBTENEMOS LOS DATOS DEL MODELO

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

input_mean = 127.5
input_std = 127.5

# ===============================================================================
#               CREACION DE CLASES PARA LA INTERFAZ GRAFICA
# ===============================================================================

class VentanaSecundaria(tk.Toplevel):
    def __init__(self, *args, callback=None, **kwargs):
        super().__init__(*args, **kwargs)

        global lista_productos, id_producto, producto, data, peso_producto, precio_unitario, precio_total, precio_suma_total, selector, n_in_productos, dataframe

        # Second Window - Configuration
        self.callback = callback
        self.config(width=480, height=320, bg='White')
        self.title('Interfaz RegistraBot')
        self.attributes("-fullscreen", True)

    # ===========================================================================
    #                          GRAPHIC USER INTERFACE
    # ===========================================================================

        # Font - Style
        self.H1 = tkFont.Font(family="Lucida Grande", size=21) #25
        self.H2 = tkFont.Font(family="Lucida Grande", size=12 ,weight="bold") #15
        self.H3 = tkFont.Font(family="Lucida Grande", size=11) #13
        self.H4 = tkFont.Font(family="Lucida Grande", size=9) #11
        self.H5 = tkFont.Font(family="Lucida Grande", size=19 ,weight="bold") #23

        # Navbar - Frame
        self.storeNameFrame = tk.Frame(self, height=45, width=480)
        self.storeNameFrame.pack_propagate(0) # don't shrink
        self.storeNameFrame.place(x=0, y=0)

        # Navbar - Title
        self.navBarlabel = tk.Label(self.storeNameFrame,text='Resumen de Venta',font=self.H1, fg='#fff', bg='red')
        self.navBarlabel.pack(fill="both", expand=1)

        # Navbar - Logo Alicorp
        self.logo = tk.PhotoImage(file='Logo-Test.png')
        self.logoReduce = self.logo.subsample(8)
        self.logolabel = tk.Label(self, image=self.logoReduce)
        self.logolabel.place(x=10, y=0)
        self.logolabel.configure(bg='red') 

        # Navbar - Date
        self.now = datetime.now()
        self.datelabel = tk.Label(self,text=str(self.now.date()),bg='red',fg='white',font=self.H4)
        self.datelabel.place(x=390, y=22)

        # Navbar - Time
        self.timelabel = tk.Label(self,text='',bg='red',fg='white',font=self.H4)
        self.timelabel.place(x=410, y=2)
        self.update_clock()

        # Table - Configuration
        self.treeview = ttk.Treeview(self, columns=("col1","col2",))

        self.treeview.column("#0", width=140)
        self.treeview.column("col1", width=100, anchor="center")
        self.treeview.column("col2", width=60, anchor="center")

        self.treeview.heading("#0", text="Producto", anchor="center")
        self.treeview.heading("col1", text="Peso/Cant",anchor="center")
        self.treeview.heading("col2", text="Precio",anchor="center")

        self.treeview.place(x=20,y=50)

        # Table - Style
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=20, bd=0, font=('Lucida Grande', 12)) # Modify the font of the body
        self.style.configure("Treeview.Heading", foreground='black' ,font=('Lucida Grande', 12,'bold')) # Modify the font of the headings
        self.style.map("Treeview", background=[('selected','#63E726')]) # Modify the font of the headings

        # Table - Load List Products
        self.mostrar_lista_productos()
        self.treeview.focus_set()
        self.treeview.focus(0)
        self.treeview.selection_set(0)
        self.actualizar_id_lista_productos()
        # print(self.treeview.get_children())
        # print(lista_productos)

        # Lable - Total Price
        self.titulo_preciosuma = tk.Label(self, text="Precio Total (S/) ", font=self.H3)
        self.titulo_preciosuma.place(x = 345, y = 90)

        self.valor_preciosuma = tk.Label(self, text="", width=7, font=self.H5 ,bg="#63E726")
        self.suma_total()
        # self.valor_preciosuma.config(text=f"{round(precio_suma_total,2)}")
        self.valor_preciosuma.place(x = 340, y = 115) 
        
        # Lable - Total State
        self.valor_estado = tk.Label(self, font=self.H3, text="ENTER PARA \nTERMINAR VENTA", justify='left')
        self.valor_estado.place(x = 340, y = 220)

        # Call Keyboad Event
        self.bind("<Key>", self.funcion_teclado_2)

    # ===============================================================================
    #                           FUNCTIONS SENCOND WINDOW
    # ===============================================================================

    # FUNCION PARA EL ACTUALIZAR EL RELOJ
    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.timelabel.configure(text=now)
        self.after(1000,self.update_clock)

    # FUNCION PARA OBTENER LA SUMA TOTAL DE PRODUCTOS
    def suma_total(self):
        global precio_suma_total
        precio_suma_total=0
        for i in range(len(lista_productos)): 
            precio_suma_total=precio_suma_total+lista_productos[i][5]
        self.valor_preciosuma.config(text=f"{round(precio_suma_total,2)}")

    # FUNCIÓN PARA MOSTRAR LOS ID DE LA LISTA DE PRODUCTOS

    def mostrar_lista_productos(self):
        for i in range(len(lista_productos)):
                self.treeview.insert("" , 100, id=f"{i}" , text=f"{lista_productos[i][1]}", values=(lista_productos[i][3],lista_productos[i][5]))

    # FUNCIÓN ACTUALIZAR LOS ID DE LA LISTA DE PRODUCTOS
    
    def actualizar_id_lista_productos(self): 
        try:
            for i in range(len(lista_productos)): 
                lista_productos[i][0]=i
                flag=i+1
                #print(i)
            id_producto=flag
            #print(id_producto)
        except:
            print("NO HAY PRODUCTO")

    #FUNCIÓN CONVERTIR LISTA EN CSV DATAFRAME

    def lista_csv(self):
        global lista_productos, dataframe
        archivo_csv = 'archivo.csv'
        with open(archivo_csv, mode='w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerows(lista_productos)
        dataframe = pd.read_csv('archivo.csv')

    #FUNCIÓN SUBIR DATA AL GOOGLE SHEET

    def subir_dataframe(self):
        # Contruimos la posicion de las celdas en formato AX:GX
        next_row = self.next_available_row(wks)
        n_elementos = len(lista_productos)
        celda=('A'+str(next_row)+':'+'I'+str(next_row+n_elementos-1))

        #Subimos todos los elementos a la ubicacion de celda obtenida
        self.pd_lista_productos = pd.DataFrame(lista_productos,columns=['id','Nombre','Marca', 'Peso (Kg)', 'Precio Unitario (S//Kg)','Precio Total (S/)','Hora','Fecha'])
        identificador = format(id(lista_productos),'n')
        self.pd_lista_productos = self.pd_lista_productos.assign(ID_Venta = identificador)
        self.products_list = self.pd_lista_productos.values.tolist()

        wks.update(celda, self.products_list)

        #wks.update(celda, lista_productos)

    def next_available_row(self,worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return len(str_list)+1


    # FUNCIÓN DE INTERFAZ DE TECLADO
    def funcion_teclado_2(self,event):
        global lista_productos, peso_producto, treeview, precio_suma_total, valor_estado, selector, n_in_productos
        # ============================================================================
        #     CUANDO SE PRESIONA "ENTER" DEBE TERMINAR LA VENTA Y SUBIR LOS ARCHIVOS
        # ============================================================================
        if (event.keysym) == "Return" or (event.keysym) == "KP_Enter":      
            # ======================================================
            # COLOCAR AQUI LA FUNCION PARA SUBIR LOS DATOS AL DRIVE
            self.subir_dataframe()

            #threading.Thread(target=self.subir_data).start()
            # ======================================================
            # DEVOLVER LOS VALORES DE LAS VARIABLES A "0"
            lista_productos = []
            producto = []
            data = []
            precio_unitario = 0
            precio_total = 0
            precio_suma_total = 0
            id_producto = 0
            selector = 0
            ventana_principal.valor_numprod.config(text="0")
            self.destroy()
        
        # ============================================================================
        #           CUANDO SE PRESIONA "BACKSPACE" SE ELIMINA UN ELEMENTO
        # ============================================================================
        if (event.keysym) == "BackSpace":
            # COMO LA FUNCION .focus() NOS BOTA EL ID DE LA FILA DEL PRODUCTO 
            curItem_id = int(self.treeview.focus())
            
            # BORRAMOS EL ELEMENTO DE LA LISTA DE PRODUCTOS 
            for i in range(len(lista_productos)):
                # BUSCAMOS EN LA LISTA DE PRODUCTO EL ID DEL PRODUCTO QUE COINCIDA CON EL ID DEL ELEMENTO SELECIONDAO
                if lista_productos[i][0] == curItem_id:
                    lista_productos.pop(i)
                    break
            
            # SELECCIONAMOS Y BORRAMOS EL ELEMENTO DE LA TABLA MOSTRADA EN LA INTERFAZ
            for j in self.treeview.get_children():
                self.treeview.delete(j)
            
            self.mostrar_lista_productos()
            # ACTUALIZAMOS LOS ID DE LAS LISTA DE PRODUCTOS PARA QUE COINCIDAN NUEVAMENTE LOS ID DE LAS FILAS
            self.actualizar_id_lista_productos()
            # SUMAMOS NUEVAMENTE TODOS LOS PRECIOS DE LOS PRODUCTOS
            self.suma_total()

            #SELECCIONAMOS EL PRIMER PRODUCTO
            try:
                self.treeview.focus(0)
                self.treeview.selection_set(0)
                selector=0
            except:
                print("no hay productos")

            print(self.treeview.get_children())
            print(lista_productos)


        # ============================================================================
        #           CUANDO SE PRESIONA "PLUS +" SE ELIMINA AGREGA UN ELEMENTO
        # ============================================================================
        if (event.keysym) == "plus" or (event.keysym) == "KP_Add":
            ventana_principal.valor_numprod.config(text=f"{len(lista_productos)}")
            self.destroy()

        # ============================================================================
        #           CUANDO SE PRESIONA "SLASH" SE SELECCIONA  UN ELEMENTO HACIA ABAJO
        # ============================================================================
        if (event.keysym) == "slash" or (event.keysym) == "KP_Divide":
            
            n_in_productos = len(lista_productos)

            if n_in_productos > selector:
                selector = selector + 1

            if selector == n_in_productos:
                selector=0

            try:
                self.treeview.focus(selector)
                self.treeview.selection_set(selector)
            except: 
                print("NO HAY PRODUCTOS")
            
            #print(selector)

       
        # ============================================================================
        #   CUANDO SE PRESIONA "ASTERIST *" SE SELECCIONA  UN ELEMENTO HACIA ARRIBA
        # ============================================================================
        if (event.keysym) == "asterisk" or (event.keysym) == "KP_Multiply":
            
            n_in_productos = len(lista_productos)

            if n_in_productos > selector:
                selector = selector - 1
 
            if selector < 0:
                selector=len(lista_productos)-1

            try:
                self.treeview.focus(selector)
                self.treeview.selection_set(selector)
            except: 
                print("NO HAY PRODUCTOS")

            #print(selector)
                    
        


class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, callback=None, **kwargs):
        
        global lista_productos, id_producto, producto, data, peso_producto, precio_unitario, precio_total, precio_suma_total, n_in_productos, precio_ref   

        super().__init__(*args, **kwargs)

        # Main Window - Configuration
        self.config(width=480, height=320, bg='white')
        self.title("Interfaz RegistraBot")
        self.attributes("-fullscreen", True)

    # ===========================================================================
    #                          GRAPHIC USER INTERFACE
    # ===========================================================================

        # Font - Style
        self.H1 = tkFont.Font(family="Lucida Grande", size=21) #25
        self.H2 = tkFont.Font(family="Lucida Grande", size=12 ,weight="bold") #15
        self.H3 = tkFont.Font(family="Lucida Grande", size=11) #13
        self.H4 = tkFont.Font(family="Lucida Grande", size=9) #11
        self.H5 = tkFont.Font(family="Lucida Grande", size=19 ,weight="bold") #23

        # NavBar - Frame
        self.storeNameFrame = tk.Frame(self, height=45, width=480)
        self.storeNameFrame.pack_propagate(0)
        self.storeNameFrame.place(x=0, y=0)

        # NavBar - Logo
        self.logo = tk.PhotoImage(file='Logo-Test.png')
        self.logoReduce = self.logo.subsample(8)
        self.logolabel = tk.Label(self, image=self.logoReduce)

        self.logolabel.place(x=10, y=0) # Logo position on display
        self.logolabel.configure(bg='red') 

        # NavBar - Title
        self.storeNamelabel = tk.Label(self.storeNameFrame,text='La Tienda de Rosita',font=self.H1, fg='#fff', bg='red')
        self.storeNamelabel.pack(fill="both", expand=1)

        # NavBar - Date
        self.now = datetime.now()
        self.datelabel = tk.Label(self,text=str(self.now.date()),bg='red',fg='white',font=self.H4)
        self.datelabel.place(x=390, y=22)

        # NavBar - Time
        self.timelabel = tk.Label(self,text='',bg='red',fg='white',font=self.H4)
        self.timelabel.place(x=410, y=2)
        self.update_clock()

        # Product detection - Label
        self.valor_producto = tk.Label(self,text='Producto a registrar', width=17, justify = "left", font=self.H2)
        self.valor_producto.place(x=270, y=65)
        self.valor_producto.configure(bg='#63E726') 

        # Peso - Lable
        self.titulo_peso = tk.Label(self,text='Peso (Kg)',font=self.H3, bg="white")
        self.titulo_peso.place(x=270, y=110)

        self.valor_peso = tk.Label(self,text='0.00', width=5, font=self.H5 ,bg="#CCCCCC")
        self.valor_peso.place(x=270, y=137)
        

        # Peso - CALL FUNCTION
        #peso_producto = self.pesar()
        self.mostrar_peso()
        #self.after(10, self.mostrar_peso)

        # Precio Unitario - Label
        self.titulo_preciou = tk.Label(self, text="Precio/Kg",font=self.H3, bg="white")
        self.titulo_preciou.place(x = 370, y = 110) 

        # Precio Unitario - Data Entry
        self.valor_preciou = tk.Entry(self, text='0.00', width=5, validate="key", font=self.H5, bg="#CCCCCC", justify = "center")
        #self.valor_preciou = tk.Entry(self, width=5, validate="key", font=self.H5, bg="#CCCCCC", justify = "center")
        #self.obtener_precio()
        vcmd = (self.valor_preciou.register(self.on_validate), '%P')
        self.valor_preciou.config(validatecommand=vcmd)
        self.valor_preciou.focus_set()
        self.valor_preciou.place(x = 370, y = 135) 

        # Precio Total - Lable
        self.titulo_preciot = tk.Label(self, text="Total (S/) ", font=self.H3, bg="white")
        self.titulo_preciot.place(x = 330, y = 190)

        self.valor_preciot = tk.Label(self,text='0.00', width=8, font=self.H5 ,bg="#63E726")
        self.valor_preciot.place(x = 300, y = 215)

        # Precio Total - Update Value
        self.after(10, self.calcular_precio)

        # Carrito de compra - Lable
        self.titulo_numprod = tk.Label(self, text="Carrito de Compra: ", font=self.H3, bg="white")
        self.titulo_numprod.place(x = 270, y = 273)

        self.valor_numprod = tk.Label(self, text="0", fg="red", font=self.H2, bg="white")
        self.valor_numprod.place(x = 440, y = 272)
        
        # Button - Exit
        self.boton_salir = tk.Button(self, text="X", height=2, width=2, command=self.destroy)
        self.boton_salir.place(x = 0, y = 280)


    # ===========================================================================
    #                          CAMERA CONFIGURATION
    # ===========================================================================
       
        # VideoCamera
        self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture(3)

        self.width, self.height = 600, 600 # Declare the width and height in variables
        # Set the width and height
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        # Init VideoCamera
        self.lblVideo = ttk.Label(self)
        self.lblVideo.place(x = 20, y = 65)
        self.open_camera()

        # EVENTO CUANDO PRECIONO UNA TECLA  
        self.bind("<Key>", self.funcion_teclado)

    # ===========================================================================
    #                         FUNCTIONS - MAIN WINDOW
    # ===========================================================================

    # FUNCION PARA EL ACTUALIZAR EL RELOJ
    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.timelabel.configure(text=now)
        self.after(1000,self.update_clock)
    
    # FUNCIONES VALIDAR ENTRADA QUE LA ENTRADA DEL PRECIO SEA UN NUMERO
    def validate(self, string):
        regex = re.compile(r"[0-9.]*$")
        result = regex.match(string)
        return (string == ""
                or (string.count('.') <= 1
                    and result is not None
                    and result.group(0) != ""))
        
    def on_validate(self, P):
        return self.validate(P)

    # FUNCIÓN PARA OBTENER EL PESO  
    # def pesar(self):
    #     peso_producto = round(random.uniform(0, 8), 2)
    #     return peso_producto

    def mostrar_peso(self):
        global peso_producto, reading
        self.valor_peso.config(text=f"{peso_producto}")
        self.after(10,self.mostrar_peso)

    def obtener_precio(self):
        global producto, precio_ref
        df = pd.read_csv('productos_db.csv')
        #print(producto[0])
        # Filtra la información del producto buscado
        informacion_producto = df[df['producto'] == producto[0]]
        # Verifica que se encontró el producto
        try:
            precio_ref = informacion_producto['precio'].iloc[0]
        except:
            precio_ref = 0
        self.valor_preciou.delete(0,100)
        self.valor_preciou.insert(0, precio_ref)
        #print(precio_ref)
        self.after(10,self.obtener_precio)

    # FUNCIÓN PARA CALCULAR PRECIO DEL PRODUCTO
    def calcular_precio(self):
        global precio_total, precio_unitario
        # OBTIENE EL PRECIO POR KG DE LA ENTRADA DE TEXTO POR EL TECLADO NUMERICO
        precio_unitario = self.valor_preciou.get()
        # OBTIENE EL PRECIO TOTAL MULTIPLICANDO EL PRECIO POR KG POR EL PESO DEL PRODUCTO
        try:
            precio_total = round(peso_producto * float(precio_unitario) ,3)
        except:
            precio_total = 0
        self.valor_preciot.config(text=f"{precio_total}")
        self.valor_preciot.pack
        self.after(10,self.calcular_precio)

    # FUNCION PARA EL RECONOCIMIENTO DE OBJETOS
    def open_camera(self):
        global lblVideo, producto

        input_data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.ret, self.frame = self.cap.read() # Capture the video frame by frame
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        h=self.frame.shape[0]
        w=self.frame.shape[1]
        h2=int((w-h)/2)
        self.frame = self.frame[0:h, h2:h2+h]
        size = (224, 224)
        self.frame = cv2.resize(self.frame, size, interpolation = cv2.INTER_AREA)
        #Convertimos la imagen en un numpy array
        image_array = np.asarray(self.frame)
        # Normalizamos la imagen
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Cargamos la imagen dentro del array
        input_data[0] = normalized_image_array
        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()
        # Retrieve detection results
        prediction = interpreter.get_tensor(output_details[0]['index'])[0] # Confidence of detected objects
        #Buscamos la posición del valor más alto del array de predicciones
        max_value = np.max(prediction)
        max_index = np.argmax(prediction)
        p_prediccion=np.amax(prediction)
        producto_det=labels_array[max_index]

        #validamos si se ha detectado 3 veces seguida el mismo producto y si es asi se rompe el loop
        if (max_value > 0.85): 
        #& (producto_det[0] != "Mano") & (producto_det[0] != "Nada"):
            producto=producto_det
            self.valor_producto.config(text=f"{producto[0]}")
        else:
            producto=["",""]
            self.valor_producto.config(text=f"-")
        
        self.frame = imutils.resize(self.frame, width=230) # Resize video
        self.captured_image = Image.fromarray(self.frame) # Capture the latest frame and transform to image
        self.photo_image = ImageTk.PhotoImage(image=self.captured_image) # Convert captured image to photoimage
        self.lblVideo.photo_image = self.photo_image # Displaying photoimage in the label
        self.lblVideo.configure(image=self.photo_image) # Configure image in the label
        self.lblVideo.after(10, self.open_camera) # Repeat the same process after every 10 seconds


    # FUNCIÓN AGREGAR PRODUCTO A LA LISTA DE COMPRA
    def agregar_producto(self):
        global lista_productos, data, precio_suma_total, id_producto, n_in_productos
        #id_producto = id_producto + 1
        #print (id_producto)
        data = [id_producto, producto[0], producto[1], peso_producto, precio_unitario, precio_total, time.strftime("%X"), time.strftime("%x")]
        #print (data)
        lista_productos.append(data)
        #print(lista_productos)
        n_in_productos=len(lista_productos)
        self.valor_numprod.config(text=f"{len(lista_productos)}")

    # FUNCIÓN DE INTERFAZ DE TECLADO
    def funcion_teclado(self,event):
        global Buzz
        #print(event.keysym)
        # CUANDO PRESIONO "ENTER" ME MUESTRA LA VENTANA SECUNDARIA CON EL RESUMEN DE VENTA
        if (event.keysym) == "Return" or (event.keysym) == "KP_Enter":
            if precio_unitario != "" :
                self.agregar_producto()
                VentanaSecundaria()
            elif len(lista_productos)>0:
                VentanaSecundaria()
                
            self.valor_preciou.delete(0, 100)
            #print("IR A VER TODOS LOS PRODUCTO")

        # CUANDO PRESIONO "+" AGREGA UN NUEVO PRODUCTO A LA LISTA DE COMPRA
        if (event.keysym) == "plus" or (event.keysym) == "KP_Add":
            #print("PRODUCTO AGREGADO")
            Buzz.start(50)
            time.sleep(0.25)
            Buzz.stop()
            if precio_unitario != "":
                self.agregar_producto()
            self.valor_preciou.delete(0, 100)


# ===============================================================================
#                                  MAIN LOOP
# ===============================================================================
"""
def my_Serial():
    global peso_producto
    #ser = serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=1)
    #ser = serial.Serial('/dev/cu.usbmodem142301', 9600, timeout=1)
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            try:
                peso_producto = float(ser.readline().decode('utf-8').rstrip())
                peso_producto = peso_producto/1000
                
            except:
                peso_producto = 0.000
            #print(peso_producto)
"""

def sensorPeso():
    global peso_producto
    while True:
        try:
            val = max(0, int(hx.get_weight(5)))
            peso_producto = round(val/1000,3)
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

if __name__ == "__main__":
    t1 = threading.Thread(target=sensorPeso)
    t1.daemon = True
    t1.start()

    ventana_principal = VentanaPrincipal()
    ventana_principal.mainloop()
