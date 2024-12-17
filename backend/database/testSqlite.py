import pandas as pd
import sqlite3
from datetime import datetime

# Leer el archivo Excel
df = pd.read_excel('raw_catalogo/raw_catalogo_productos.xlsx', sheet_name='Hoja 1')

# Añadir una columna con la fecha y hora actuales
df['insert_date'] = datetime.now()

# Conectar a la base de datos
conn = sqlite3.connect('BD_RegistraBOT.db')
cursor = conn.cursor()

# Eliminar todo el contenido de la tabla
cursor.execute('DELETE FROM tb_catalogo_productos')
conn.commit()

# Resetear el contador de AUTOINCREMENT
cursor.execute('DELETE FROM sqlite_sequence WHERE name="tb_catalogo_productos"')
conn.commit()

# Insertar los datos del DataFrame en la tabla de la base de datos
df.to_sql('tb_catalogo_productos', conn, if_exists='append', index=False)

# Cerrar la conexión
conn.close()