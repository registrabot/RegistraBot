import os
import time
import requests  # Librería para HTTP
import json
import sqlite3
from datetime import datetime

# Configuración de ThingsBoard
THINGSBOARD_HOST = 'https://thingsboard.cloud'
ACCESS_TOKEN = 'lGJjHAKOtOfGMkgkoMJK'
TELEMETRY_URL = f"{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry"

DB_PATH = '/home/pato/RegistraBot/backend/database/BD_RegistraBOT.db'

def send_telemetry(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(TELEMETRY_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print(f"✔ Telemetría enviada correctamente: {data}")
        else:
            print(f"❌ Error al enviar telemetría: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"⚠ Error enviando telemetría: {e}")

def main():
    try:
        print("⏳ Procesando datos...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = '''SELECT * FROM tb_registro_ventas A 
                   LEFT JOIN tb_catalogo_productos B 
                   ON TRIM(REPLACE(REPLACE(A.sku, '\n', ''), '\r', '')) = B.sku 
                   WHERE A.estado_carga = 0'''
        cursor.execute(query)
        tb_catalogo_productos = cursor.fetchall()

        if not tb_catalogo_productos:
            print("✅ No hay nuevos datos para enviar.")
            return

        for producto in tb_catalogo_productos:
            # Formato correcto para ThingsBoard
            data = [{
                'ts': int(datetime.now().timestamp()*1000),
                'values': {
                    'id': producto[0],
                    'id_venta': producto[1],
                    'id_bodega': producto[2],
                    'sku': producto[3],
                    'cantidad': producto[4],
                    'precio_unitario': producto[5],
                    'precio_total': producto[6],
                    'medio_pago': producto[7],
                    'date': producto[8]
                }
            }]

            print(f"📤 Enviando: {data}")
            send_telemetry(data)

            # Marcar el registro como enviado
            update_query = '''UPDATE tb_registro_ventas SET estado_carga = 1 WHERE id = ?'''
            cursor.execute(update_query, (producto[0],))
            time.sleep(0.5)  # Pequeña pausa entre envíos


        conn.commit()
        print("✅ Envío de datos completado.")

    except Exception as e:
        print(f"❌ Error procesando datos: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
