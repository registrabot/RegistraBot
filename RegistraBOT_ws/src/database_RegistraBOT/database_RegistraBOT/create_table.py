import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('BD_RegistraBOT.db')
cursor = conn.cursor()

# Crear la tabla con la nueva columna insert_date
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_catalogo_productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        categoria_producto TEXT NOT NULL,
        subcategoria_producto TEXT NOT NULL,
        tipo_envase TEXT NOT NULL,
        marca TEXT NOT NULL,
        tamaño INTEGER,
        nombre_producto TEXT NOT NULL,
        nombre_producto_abreviado TEXT,
        path_image TEXT NOT NULL,
        insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
