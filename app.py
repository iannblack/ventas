import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Aquí realizo la configuración de la base de datos.
# Uso 'root' como usuario y me conecto a la base de datos 'ventas' en localhost, sin contraseña.
DATABASE_URL = "mysql+pymysql://root:@localhost/ventas"  
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Aquí defino la estructura de la tabla 'sales' que voy a usar en la base de datos.
# Cada atributo de esta clase corresponde a una columna en la tabla de ventas.
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)  # 'id' será la clave primaria de la tabla.
    product = Column(String(255))  # 'product' es una columna de texto con un límite de 255 caracteres.
    quantity = Column(Integer)  # 'quantity' es un número entero que representa la cantidad de producto.
    price = Column(Float)  # 'price' es un número decimal que almacena el precio del producto.
    date = Column(Date)  # 'date' es una columna que almacena la fecha de la venta.

# Aquí le digo a SQLAlchemy que cree la tabla 'sales' en la base de datos si no existe.
Base.metadata.create_all(engine)

# Configuro la sesión para interactuar con la base de datos.
Session = sessionmaker(bind=engine)
session = Session()

# Esta función carga los datos desde un archivo CSV a la base de datos.
# El CSV debe tener las columnas 'product', 'quantity', 'price' y 'date'.
def load_data_to_db(csv_file):
    df = pd.read_csv(csv_file)  # Leo el archivo CSV con pandas.
    for index, row in df.iterrows():
        sale = Sale(
            product=row['product'],  # Cargo el nombre del producto.
            quantity=row['quantity'],  # Cargo la cantidad de producto vendida.
            price=row['price'],  # Cargo el precio de cada producto.
            date=datetime.strptime(row['date'], "%Y-%m-%d")  # Conviero la fecha de string a objeto datetime.
        )
        session.add(sale)  # Agrego la venta a la sesión.
    session.commit()  # Guardo todos los cambios en la base de datos.

# Esta función genera el gráfico de barras con las ventas totales por producto.
def generate_sales_graph():
    # Aquí consulto las ventas, calculando las ventas totales (cantidad * precio) por producto.
    results = session.query(Sale.product, (Sale.quantity * Sale.price).label('total_sales')).group_by(Sale.product).all()
    
    # Extraigo los nombres de los productos y las ventas totales.
    products = [r[0] for r in results]
    total_sales = [r[1] for r in results]

    # Creo el gráfico de barras.
    plt.bar(products, total_sales)
    plt.xlabel('Producto')  # Etiqueta del eje X.
    plt.ylabel('Ventas Totales')  # Etiqueta del eje Y.
    plt.title('Ventas Totales por Producto')  # Título del gráfico.
    plt.xticks(rotation=45)  # Roto las etiquetas del eje X para que se vean mejor.
    plt.tight_layout()  # Ajusto el diseño para que todo se vea bien.
    plt.savefig('sales_graph.png')  # Guardamos el gráfico como una imagen.
    plt.show()  # Muestra el gráfico.

# Esta función filtra las ventas por un rango de fechas.
# Puedo usarla para ver las ventas realizadas en un periodo específico.
def filter_sales_by_date(start_date, end_date):
    # Aquí filtro las ventas que ocurrieron entre las fechas de inicio y fin.
    filtered_sales = session.query(Sale).filter(Sale.date.between(start_date, end_date)).all()
    # Imprimo los resultados filtrados.
    for sale in filtered_sales:
        print(f"Producto: {sale.product}, Cantidad: {sale.quantity}, Precio: {sale.price}, Fecha: {sale.date}")

# Cargamos los datos desde un archivo CSV (Tenemos que descomentar la siguiente línea si tenemos el archivo CSV).
# load_data_to_db('ventas.csv')

# Filtramos ventas entre dos fechas (Tenemos que descomentar y ajustar las fechas si queremos usarlo).
# filter_sales_by_date(datetime(2023, 1, 1), datetime(2023, 12, 31))

# Generamos el gráfico con las ventas totales por producto.
generate_sales_graph()
