import pandas as pd
from sqlalchemy import create_engine

# Configuración de la conexión a la base de datos MySQL
username = 'root'  # Cambia por tu usuario si es diferente
password = ''      # No usamos contraseña en este caso, por lo que dejamos esto vacío
host = 'localhost' # Usamos localhost ya que estamos trabajando de forma local
database = 'ventas'  # La base de datos donde cargaremos los datos

# Conexión a la base de datos
engine = create_engine(f'mysql+pymysql://root:@localhost/ventas')

# Cargar el archivo CSV
df = pd.read_csv('ventas.csv')

# Verifica si los datos se cargaron correctamente
print(df.head())  # Esto muestra las primeras filas del archivo

# Cargamos los datos a la tabla "sales" de la base de datos
df.to_sql('sales', con=engine, if_exists='replace', index=False)

print("Datos cargados correctamente a la base de datos.")
