import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('BD_RegistraBOT.db')

# Crear un cursor para interactuar con la base de datos
cursor = conn.cursor()

# Definir el nombre de la tabla que quieres eliminar
nombre_tabla1 = 'tb_catalogo_productos'
nombre_tabla2 = 'tb_registro_ventas'
# Ejecutar el comando DROP TABLE
cursor.execute(f'DROP TABLE IF EXISTS {nombre_tabla1}')
cursor.execute(f'DROP TABLE IF EXISTS {nombre_tabla2}')
conn.commit()

# Cerrar la conexión
conn.close()