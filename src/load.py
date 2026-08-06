import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def obtener_motor_conexion():
    """
    Crea y retorna un motor de conexión (Engine) de SQLAlchemy 
    utilizando las credenciales del archivo .env
    """
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB")

    # Formato de la URL de conexión de SQLAlchemy:
    # postgresql://usuario:contraseña@host:puerto/nombre_bd
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    # Crear el engine de SQLAlchemy
    engine = create_engine(connection_string)
    return engine


def cargar_dataframe_a_postgres(df: pd.DataFrame, nombre_tabla: str = "precipitaciones_diarias") -> bool:
    """
    Inserta un DataFrame de Pandas en una tabla de la base de datos PostgreSQL.

    Parámetros:
      - df (pd.DataFrame): DataFrame transformado listo para carga.
      - nombre_tabla (str): Nombre de la tabla destino en PostgreSQL.

    Retorna:
      - bool: True si la carga fue exitosa.
    """
    if df.empty:
        print("⚠️ El DataFrame está vacío. No hay datos que cargar.")
        return False

    engine = obtener_motor_conexion()

    try:
        print(f"Conectando a PostgreSQL y cargando {len(df)} registros en la tabla '{nombre_tabla}'...")

        # to_sql se encarga de crear la tabla e insertar las filas
        # if_exists='append': Si la tabla ya existe, agrega las nuevas filas al final
        # index=False: Evita guardar el índice numérico propio de Pandas como una columna
        df.to_sql(
            name=nombre_tabla,
            con=engine,
            if_exists="append",
            index=False
        )

        print(f"¡Carga exitosa! Se guardaron {len(df)} filas en PostgreSQL.")
        return True

    except Exception as error:
        print(f"❌ Error al cargar los datos en PostgreSQL: {error}")
        raise


# Bloque de prueba local combinando Extract + Transform + Load
if __name__ == "__main__":
    from extract import extraer_datos_precipitacion
    from transform import transformar_datos_precipitacion

    print("--- Probando Pipeline Completo: Extract -> Transform -> Load ---")

    # Coordenadas de Ovalle
    LAT_OVALLE = -30.5983
    LON_OVALLE = -71.2003

    try:
        # 1. Extract
        datos_crudos = extraer_datos_precipitacion(
            latitud=LAT_OVALLE,
            longitud=LON_OVALLE,
            fecha_inicio="2026-06-01",
            fecha_fin="2026-06-30"
        )

        # 2. Transform
        df_clima = transformar_datos_precipitacion(datos_crudos, nombre_localidad="Ovalle")

        # 3. Load
        cargar_dataframe_a_postgres(df_clima, nombre_tabla="precipitaciones_diarias")

    except Exception as e:
        print(f"\n❌ Ocurrió un error en la prueba de carga: {e}")