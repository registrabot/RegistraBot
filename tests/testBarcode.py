import sys

parent_dir = '/home/pato/RegistraBot/backend/'
sys.path.append(parent_dir)

from modules.barcode_module.barcode_module import BarcodeScanner

scanner = BarcodeScanner(port_='/dev/hidraw1')



while True:
    print(scanner.scan())  