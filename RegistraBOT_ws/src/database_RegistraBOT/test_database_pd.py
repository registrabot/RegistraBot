import sqlite3
import pandas as pd
import os

# Ruta a la base de datos
db_path = 'BD_RegistraBOT.db'

# Verificar si el archivo de la base de datos existe
if not os.path.exists(db_path):
    print(f"Error: La base de datos en la ruta {db_path} no existe.")
else:
    try:
        # Conectar a la base de datos SQLite
        bdRegistrabot = sqlite3.connect(db_path)
        print("Conexión a la base de datos establecida con éxito.")

        # Leer la tabla en un DataFrame de pandas
        df_product_name = pd.read_sql_query("SELECT * FROM tb_catalogo_productos", bdRegistrabot)
        print("Datos leídos con éxito de la tabla tb_catalogo_productos.")

        # Mostrar las columnas para verificar que 'sku' existe
        print("Columnas del DataFrame:", df_product_name.columns)

        # Mostrar algunos valores de la columna 'sku'
        print("Valores de la columna 'sku':", df_product_name['sku'].head())

        # Supongamos que self.product_name contiene el valor a buscar
        product_name = 'GR-FR-BS-GRA-000-001'  # Asegúrate de ajustar esto al valor correcto

        # Verificar el valor de product_name
        print("Valor de product_name:", product_name)

        # Filtrar el DataFrame por el valor de 'sku'
        product_name_df = df_product_name[df_product_name['sku'].str.strip().str.lower() == product_name.strip().lower()]

        # Verificar el DataFrame filtrado
        print(product_name_df)

    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    except pd.io.sql.DatabaseError as e:
        print(f"Error al ejecutar la consulta SQL: {e}")
    finally:
        # Cerrar la conexión a la base de datos
        if bdRegistrabot:
            bdRegistrabot.close()
            print("Conexión a la base de datos cerrada.")
