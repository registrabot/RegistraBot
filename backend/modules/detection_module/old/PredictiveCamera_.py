import cv2
import tflite_runtime.interpreter as tflite
import numpy as np

class PredictiveCamera:
    def __init__(self, model_path, label_path):
        self.model_path = model_path
        self.label_path = label_path
        self.labels = self.load_labels(label_path)
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("No se pudo abrir la cámara.")

    def load_labels(self, label_path):
        self.labels_array = []
        try:
            with open(label_path) as labels:
                for line in labels:
                    x = line.split(", ")
                    producto = x[0].split(" ", 1)[1]
                    self.labels_array.append([producto])
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo de etiquetas: {label_path}")
        return self.labels_array

    def prepare_image(self, frame):
        input_details = self.interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        input_data = np.ndarray(input_shape, dtype=np.uint8)
        
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Center crop
        h, w = rgb_frame.shape[:2]
        h2 = int((w - h) / 2)
        rgb_frame = rgb_frame[0:h, h2:h2 + h]
        
        # Resize to input shape
        rgb_frame = cv2.resize(rgb_frame, (input_shape[2], input_shape[1]), interpolation=cv2.INTER_AREA)
        
        # Load image into input array
        input_data[0] = rgb_frame
        
        return input_data
    
    def interpret_output(self, output_data):
        output_data = output_data.astype('float64') / 100
        max_value = np.max(output_data)
        max_index = np.argmax(output_data)
        producto_det = self.labels_array[max_index]
        
        if max_value > 0.85:
            return producto_det[0], max_value
        else:
            tres_valores_altos = self.tres_valores_mas_altos(output_data)
            posiciones_tres_valores_altos = self.posiciones_tres_valores_mas_altos(output_data)
            productos_seleccionados = self.productos_por_posiciones(self.labels_array, posiciones_tres_valores_altos)
            return tres_valores_altos, productos_seleccionados

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None, None

        input_data = self.prepare_image(frame)

        input_details = self.interpreter.get_input_details()
        self.interpreter.set_tensor(input_details[0]['index'], input_data)
        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()
        output_data = self.interpreter.get_tensor(output_details[0]['index'])[0]
        
        result = self.interpret_output(output_data)

        if isinstance(result[0], float):  # Check if the result is a single value and product name
            product_name, max_value = result
            return frame, product_name, max_value
        else:
            tres_valores_altos, productos_seleccionados = result
            return frame, tres_valores_altos, productos_seleccionados
    
    def tres_valores_mas_altos(self, array):
        # Ordenar el array en orden descendente
        array_ordenado = sorted(array, reverse=True)
        # Tomar los tres primeros elementos
        tres_valores = array_ordenado[:3]
        return tres_valores

    def posiciones_tres_valores_mas_altos(self, array):
        # Enumerar los elementos del array junto con sus índices
        indices_y_valores = list(enumerate(array))
        # Ordenar los elementos del array según sus valores en orden descendente
        indices_ordenados = sorted(indices_y_valores, key=lambda x: x[1], reverse=True)
        # Tomar los índices de los tres primeros elementos
        tres_indices = [indice for indice, valor in indices_ordenados[:3]]
        return tres_indices

    def productos_por_posiciones(self, array_productos, posiciones):
        productos_seleccionados = []
        for pos in posiciones:
            if pos < len(array_productos):
                productos_seleccionados.append(array_productos[pos])
            else:
                print(f"Índice {pos} fuera de rango.")
        return productos_seleccionados
    
    
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()