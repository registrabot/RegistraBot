import cv2
import tensorflow as tf
import numpy as np

class PredictiveCamera:
    def __init__(self, model_path, label_path):
        self.model_path = model_path
        self.label_path = label_path
        self.labels = self.load_labels(label_path)
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.cap = cv2.VideoCapture(0)

    def load_labels(self, label_path):
        self.labels_array = []
        with open(label_path) as labels:
            for line in labels:
                x = line.split(", ")
                producto = x[0].split(" ", 1)[1]
                #marca = x[1].split("\n")[0]
                #self.labels_array.append([producto, marca])
                self.labels_array.append([producto])
        return self.labels_array

    def prepare_image(self, frame):
        input_details = self.interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        input_data = np.ndarray(input_shape, dtype=np.float32)
        
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Center crop
        h, w = rgb_frame.shape[:2]
        h2 = int((w - h) / 2)
        rgb_frame = rgb_frame[0:h, h2:h2 + h]
        
        # Resize to input shape
        rgb_frame = cv2.resize(rgb_frame, (input_shape[2], input_shape[1]), interpolation=cv2.INTER_AREA)
        
        # Normalize image
        normalized_image_array = (rgb_frame.astype(np.float32) / 127.0) - 1
        
        # Load image into input array
        input_data[0] = normalized_image_array
        
        return input_data

    def interpret_output(self, output_data):
        max_value = np.max(output_data)
        max_index = np.argmax(output_data)
        producto_det = self.labels_array[max_index]
        if max_value > 0.85:
           return producto_det[0]

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        input_data = self.prepare_image(frame)

        input_details = self.interpreter.get_input_details()
        self.interpreter.set_tensor(input_details[0]['index'], input_data)
        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()
        output_data = self.interpreter.get_tensor(output_details[0]['index'])[0]
        
        product_name = self.interpret_output(output_data)

        tres_valores_altos = self.tres_valores_mas_altos(output_data)
        print("Los tres valores más altos son:", tres_valores_altos)

        posiciones_tres_valores_altos = self.posiciones_tres_valores_mas_altos(output_data)
        print("Las posiciones de los tres valores más altos son:", posiciones_tres_valores_altos)

        productos_seleccionados = self.productos_por_posiciones(self.labels_array, posiciones_tres_valores_altos)
        print("Productos seleccionados:", productos_seleccionados)

        return frame, product_name
    
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
        productos_seleccionados = [array_productos[pos] for pos in posiciones]
        return productos_seleccionados
    
    
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
