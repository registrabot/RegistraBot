import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('BD_RegistraBOT.db')
cursor = conn.cursor()


## =================================================
##       CREATE TABLE tb_catalogo_productos
## =================================================
# Crear la tabla con la nueva columna insert_date
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_catalogo_productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        nombre_producto TEXT NOT NULL,
        categoria_producto TEXT NULL,
        subcategoria_producto TEXT NULL,
        tamano REAL,
        unidad_medida TEXT,
        marca TEXT NULL,
        tipo_envase TEXT NULL,
        empresa_fabricante TEXT,
        path_image TEXT NOT NULL,
        insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

## =================================================
##       CREATE TABLE tb_registro_ventas
## =================================================
# Crear la tabla con la nueva columna insert_date
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_registro_ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER  NOT NULL,
        id_bodega TEXT NOT NULL,
        sku TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario NUMERIC NOT NULL,       
        precio_total NUMERIC NOT NULL,
        medio_pago TEXT NOT NULL,
        insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado_carga INTEGER NOT NULL
    )
''')

conn.commit()
conn.close()
