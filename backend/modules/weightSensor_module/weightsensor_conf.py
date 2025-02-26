import RPi.GPIO as GPIO
from weightsensor_module.hx711 import HX711
import time


# ==============================
#    Weight Sensor Parameters
# ==============================

class WeightSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.hx = HX711(26, 20)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(48.87602840553819)
        self.hx.reset()
        self.hx.tare()
    
    def get_weight(self, time_sleep):
        val = max(0, int(self.hx.get_weight(5)))
        print(val)
        peso_producto = round(val/2239,3)
        self.hx.power_down()
        self.hx.power_up()
        time.sleep(time_sleep)
        return peso_producto
    
    def clean_and_exit(self):
        GPIO.cleanup()
