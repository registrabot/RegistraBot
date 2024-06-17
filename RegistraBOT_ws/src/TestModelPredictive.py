from object_detection_module.PredictiveCamera import PredictiveCamera

if __name__ == "__main__":
    # Uso de la clase
    model_path = "modelo-bodega1/detect.tflite"
    #labels_path = "modelo-bodega1/labels.txt"
    labels_path = "modelo-bodega1/labelmap.txt"

    detector = PredictiveCamera(model_path, labels_path)
    detector.detect()
