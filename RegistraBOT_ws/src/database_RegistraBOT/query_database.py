import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('BD_RegistraBOT.db')
cursor = conn.cursor()

# Consultar datos
cursor.execute('SELECT * FROM tb_catalogo_productos')

# Obtener todos los resultados
tb_catalogo_productos = cursor.fetchall()

for productos in tb_catalogo_productos:
    print(productos)

# Cerrar la conexión
conn.close()