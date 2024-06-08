import cv2
import numpy as np
import tensorflow as tf

class PredictiveCamera:
    def __init__(self, model_path, labels_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        self.labels_array = []
        with open(labels_path) as labels:
            for line in labels:
                x = line.split(", ")
                producto = x[0].split(" ", 1)[1]
                marca = x[1].split("\n")[0]
                self.labels_array.append([producto, marca])
        
    def prepare_image(self, frame):
        input_shape = self.input_details[0]['shape']
        input_data = np.ndarray(input_shape, dtype=np.float32)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h = rgb_frame.shape[0]
        w = rgb_frame.shape[1]
        h2 = int((w - h) / 2)
        rgb_frame = rgb_frame[0:h, h2:h2 + h]
        rgb_frame = cv2.resize(rgb_frame, (input_shape[2], input_shape[1]), interpolation=cv2.INTER_AREA)
        # Convertimos la imagen en un numpy array
        image_array = np.asarray(rgb_frame)
        # Normalizamos la imagen
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Cargamos la imagen dentro del array
        input_data[0] = normalized_image_array
        return input_data
    
    def interpret_output(self, output_data):
        max_value = np.max(output_data)
        max_index = np.argmax(output_data)
        p_prediccion = np.amax(output_data)
        producto_det = self.labels_array[max_index]
        if (max_value > 0.85): 
            print(producto_det)
    
    def detect(self):
        cap = cv2.VideoCapture(0)
        while True:
            # Capturar un frame de la cámara
            ret, frame = cap.read()
            if not ret:
                break

            # Preparar la imagen de entrada
            input_data = self.prepare_image(frame)

            # Establecer los datos de entrada
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

            # Ejecutar el intérprete
            self.interpreter.invoke()

            # Obtener los resultados de salida
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

            # Interpretar los resultados de salida
            self.interpret_output(output_data)

            # Mostrar el frame
            cv2.imshow('Teachable Machine en tiempo real', frame)

            # Salir si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar la cámara y cerrar todas las ventanas
        cap.release()
        cv2.destroyAllWindows()

