## keypad_class.py

import RPi.GPIO as GPIO
import keypad_module.keypad_lib as keypad_lib

class KeypadController:
    def __init__(self):
        self.ROWS = 4
        self.COLS = 4
        self.keys = ['1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*', '0', '#', 'D']
        self.rowsPins = [27, 22, 0, 5]
        self.colsPins = [6, 13, 19, 1]
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def get_key(self):
        keypad = keypad_lib.Keypad(self.keys, self.rowsPins, self.colsPins, self.ROWS, self.COLS)
        keypad.setDebounceTime(10)
        while True:
            key = keypad.getKey()
            if key != keypad.NULL:
                return key

    def enter_price(self, price_value_str):
        key = self.get_key()
        if key.isdigit():
            price_value_str += key 
            price_value_float = float(price_value_str)
            return price_value_float, price_value_str
        elif key == '*':
            if price_value_str.count('.') < 1:
                price_value_str += "."
                if price_value_str.startswith("."):
                    price_value_str = "0."
                price_value_float = float(price_value_str)
                return price_value_float, price_value_str
            else:
                price_value_float = float(price_value_str)
                return price_value_float, price_value_str
        elif key == 'A':
            price_value_str = price_value_str[:-1]
            if price_value_str == "":
                price_value_float = 0
            else:
                price_value_float = float(price_value_str)
            return price_value_float, price_value_str
        else:
            
            price_value_float = float(price_value_str)
            #print(price_value_str)
            #print(price_value_float)
            return price_value_float, price_value_str

