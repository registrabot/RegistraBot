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

    def load_labels(self, label_path):
        self.labels_array = []
        try:
            with open(label_path) as labels:
                for line in labels:
                    x = line.split(", ")
                    sku = x[0].split(" ", 1)[1]
                    self.labels_array.append([sku])
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo de etiquetas: {label_path}")
        return self.labels_array
    
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()