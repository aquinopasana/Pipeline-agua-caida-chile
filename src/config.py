import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env al entorno de ejecución
load_dotenv()

# Acceder a las variables usando os.getenv()
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
API_URL = os.getenv("WEATHER_API_URL")

# Prueba para verificar que todo se lee correctamente
if __name__ == "__main__":
    print("--- Configuración Cargada ---")
    print(f"Base de datos: {DB_NAME}")
    print(f"Usuario DB: {DB_USER}")
    print(f"Host: {DB_HOST}:{DB_PORT}")
    print(f"URL API: {API_URL}")