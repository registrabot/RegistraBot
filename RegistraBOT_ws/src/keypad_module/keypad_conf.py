import RPi.GPIO as GPIO
import keypad_module.keypad_class as keypad_class

class KeypadModule:
    def __init__(self):
        self.price_value_str = ""
        self.keys =  [   '1','2','3','A',    #key code
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
        self.rowsPins = [27, 22, 0, 5]
        self.colsPins = [6, 13, 19, 1]
        self.ROWS = 4
        self.COLS = 4
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def get_key(self):
        keypad = keypad_class.Keypad(self.keys, self.rowsPins, self.colsPins,self.ROWS, self.COLS)
        keypad.setDebounceTime(50)
        while True:
            key = keypad.getKey()
            if key != keypad.NULL:
                return key

    def enter_price(self, numero_tecla=None, numero_unido=None):
        if numero_tecla is None or numero_unido is None:
            key = self.get_key()
        else:
            key = self.get_key()  # Use self.get_key() if get_key is a method of the class

        if numero_tecla is not None and numero_unido is not None:
            if key.isdigit():
                numero_tecla.append(key)
                numero_unido = ''.join(numero_tecla)
                precio_unitario = float(numero_unido)
            elif key == '*':
                if '.' not in numero_unido:
                    numero_tecla.append('.')
                    numero_unido = ''.join(numero_tecla)
                    precio_unitario = float(numero_unido)
            elif key == 'A':
                if numero_tecla:
                    numero_tecla.pop()
                    numero_unido = ''.join(numero_tecla)
                    precio_unitario = float(numero_unido) if numero_unido else 0

            print('ObtenerTecla: ', numero_unido)
            return precio_unitario

        else:
            if key.isdigit():
                self.price_value_str += key
            elif key == '*':
                if self.price_value_str.count('.') < 1:
                    self.price_value_str += "."
                    if self.price_value_str.startswith("."):
                        self.price_value_str = "0."
            elif key == 'A':
                self.price_value_str = self.price_value_str[:-1] if self.price_value_str else ""

            return float(self.price_value_str) if self.price_value_str else 0.0