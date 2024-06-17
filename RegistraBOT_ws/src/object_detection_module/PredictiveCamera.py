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
        with open(label_path, 'r') as f:
            return {i: line.strip() for i, line in enumerate(f.readlines())}

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        input_shape = input_details[0]['shape']
        input_data = cv2.resize(frame, (input_shape[1], input_shape[2]))
        input_data = np.expand_dims(input_data, axis=0)
        input_data = (np.float32(input_data) - 127.5) / 127.5

        self.interpreter.set_tensor(input_details[0]['index'], input_data)
        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        predicted_label_index = np.argmax(output_data[0])
        product_name = self.labels[predicted_label_index]

        return frame, product_name

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
