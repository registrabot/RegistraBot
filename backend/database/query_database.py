import sqlite3
import pandas as pd
import sys
# Conectar a la base de datos
conn = sqlite3.connect('BD_RegistraBOT.db')
cursor = conn.cursor()

# SKUS
sku = ['GR-VR-BS-GRA-000-001','GR-VR-BS-GRA-000-002','GR-VR-BS-GRA-000-003']
# Consultar datos
#cursor.execute('SELECT * FROM tb_catalogo_productos WHERE sku = ''GR-VR-BS-GRA-000-005''')
#cursor.execute('SELECT * FROM tb_catalogo_productos WHERE sku = ?', ('GR-VR-BS-GRA-000-005',))
#query = 'SELECT * FROM tb_catalogo_productos WHERE sku IN ({})'.format(','.join('?' * len(sku)))



"""ventas = [
    (1, 'B001', 'SKU123', 1.5, 2, 10.0, 20.0, 'Tarjeta', 'Completado'),
    (1, 'B002', 'SKU124', 2.0, 1, 15.0, 15.0, 'Efectivo', 'Pendiente'),
    (2, 'B003', 'SKU125', 0.5, 5, 8.0, 40.0, 'Transferencia', 'Completado')
]

# Insertar datos en la tabla
cursor.executemany('''
    INSERT INTO tb_registro_ventas (id_venta, id_bodega, sku, peso, cantidad, precio_unitario, precio_total, medio_pago, estado_venta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', ventas)

# Confirmar los cambios
conn.commit()"""

#df = pd.read_sql_query('SELECT * FROM tb_registro_ventas', conn)
#print(df)
query = 'SELECT * FROM tb_registro_ventas'
#cursor.execute(query, sku)
cursor.execute(query)
# Obtener todos los resultados
tb_catalogo_productos = cursor.fetchall()

for productos in tb_catalogo_productos:
    print(productos)

# Cerrar la conexión


query = 'SELECT * FROM tb_catalogo_productos'
#cursor.execute(query, sku)
cursor.execute(query)
# Obtener todos los resultados
tb_catalogo_productos = cursor.fetchall()

for productos in tb_catalogo_productos:
    print(productos)

# Cerrar la conexión

conn.close()