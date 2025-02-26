import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
import os

class PredictiveCamera:
    def __init__(self, models_path, labels_path):
        self.models_path = models_path
        self.labels_path = labels_path
        self.models, self.labels = self.load_models_and_labels(models_path, labels_path)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("No se pudo abrir la cámara.")

    def load_models_and_labels(self, models_path, labels_path):
        models = []
        labels = []
        model_files = sorted(os.listdir(models_path))
        label_files = sorted(os.listdir(labels_path))

        for model_file, label_file in zip(model_files, label_files):
            model_file_path = os.path.join(models_path, model_file)
            label_file_path = os.path.join(labels_path, label_file)

            interpreter = tflite.Interpreter(model_path=model_file_path)
            interpreter.allocate_tensors()
            models.append(interpreter)
            labels.append(self.load_labels(label_file_path))

        return models, labels

    def load_labels(self, label_path):
        labels_array = []
        try:
            with open(label_path) as labels:
                for line in labels:
                    x = line.split(", ")
                    producto = x[0].split(" ", 1)[1]
                    labels_array.append(producto)
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo de etiquetas: {label_path}")
        return labels_array

    def prepare_image(self, frame, interpreter):
        input_details = interpreter.get_input_details()
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
    
    def interpret_output(self, output_data_list):
        combined_output = np.concatenate(output_data_list)
        max_value = np.max(combined_output)
        max_index = np.argmax(combined_output)

        total_labels = sum(len(lbl) for lbl in self.labels)
        model_index = 0
        cumulative_index = max_index

        for labels in self.labels:
            if cumulative_index < len(labels):
                break
            model_index += 1
            cumulative_index -= len(labels)
        
        producto_det = self.labels[model_index][cumulative_index]
        
        if max_value > 0.85:
            return producto_det, max_value
        else:
            tres_valores_altos = self.tres_valores_mas_altos(combined_output)
            posiciones_tres_valores_altos = self.posiciones_tres_valores_mas_altos(combined_output)
            productos_seleccionados = self.productos_por_posiciones(self.labels, posiciones_tres_valores_altos)
            return tres_valores_altos, productos_seleccionados

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None, None

        output_data_list = []
        for interpreter in self.models:
            input_data = self.prepare_image(frame, interpreter)

            input_details = interpreter.get_input_details()
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            output_details = interpreter.get_output_details()
            output_data = interpreter.get_tensor(output_details[0]['index'])[0]
            output_data_list.append(output_data)
        
        result = self.interpret_output(output_data_list)

        if isinstance(result[0], float):  # Check if the result is a single value and product name
            product_name, max_value = result
            return frame, product_name, max_value
        else:
            tres_valores_altos, productos_seleccionados = result
            return frame, tres_valores_altos, productos_seleccionados
    
    def tres_valores_mas_altos(self, array):
        array_ordenado = sorted(array, reverse=True)
        tres_valores = array_ordenado[:3]
        return tres_valores

    def posiciones_tres_valores_mas_altos(self, array):
        indices_y_valores = list(enumerate(array))
        indices_ordenados = sorted(indices_y_valores, key=lambda x: x[1], reverse=True)
        tres_indices = [indice for indice, valor in indices_ordenados[:3]]
        return tres_indices

    def productos_por_posiciones(self, all_labels, posiciones):
        productos_seleccionados = []
        total_labels = sum(len(lbl) for lbl in all_labels)

        for pos in posiciones:
            model_index = 0
            cumulative_index = pos

            for labels in all_labels:
                if cumulative_index < len(labels):
                    productos_seleccionados.append(labels[cumulative_index])
                    break
                model_index += 1
                cumulative_index -= len(labels)

        return productos_seleccionados

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()