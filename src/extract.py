import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno (por si la URL base está definida ahí)
load_dotenv()

# URL base por defecto si no está en el .env
DEFAULT_API_URL = "https://archive-api.open-meteo.com/v1/archive"


def extraer_datos_precipitacion(
    latitud: float,
    longitud: float,
    fecha_inicio: str,
    fecha_fin: str,
    zona_horaria: str = "America/Santiago"
) -> dict:
    """
    Consulta la API de Open-Meteo y extrae la cantidad diaria de agua caída (mm)
    para las coordenadas y rango de fechas especificados.

    Parámetros:
      - latitud (float): Latitud de la localidad (ej: -30.5983 para Ovalle).
      - longitud (float): Longitud de la localidad (ej: -71.2003 para Ovalle).
      - fecha_inicio (str): Fecha de inicio en formato 'YYYY-MM-DD'.
      - fecha_fin (str): Fecha de fin en formato 'YYYY-MM-DD'.
      - zona_horaria (str): Zona horaria para agrupar los días.

    Retorna:
      - dict: Respuesta en formato JSON entregada por la API.
    """
    base_url = os.getenv("WEATHER_API_URL", DEFAULT_API_URL)

    # Parámetros que exige la API de Open-Meteo
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": fecha_inicio,
        "end_date": fecha_fin,
        "daily": "precipitation_sum",  # Pide la suma diaria de precipitación (mm)
        "timezone": zona_horaria
    }

    try:
        print(f"Obteniendo datos meteorológicos desde {fecha_inicio} hasta {fecha_fin}...")
        response = requests.get(base_url, params=params, timeout=10)
        
        # Lanza una excepción si el status code HTTP no es 200 (OK)
        response.raise_for_status()

        datos = response.json()
        print("¡Extracción exitosa!")
        return datos

    except requests.exceptions.RequestException as error:
        print(f"Error al conectar con la API de Open-Meteo: {error}")
        raise


# Bloque de prueba local para verificar que funcione
if __name__ == "__main__":
    # Coordenadas de prueba (Ovalle, Región de Coquimbo)
    LAT_OVALLE = -30.5983
    LON_OVALLE = -71.2003
    FECHA_INICIO = "2026-07-01"
    FECHA_FIN = "2026-07-31"

    datos_crudos = extraer_datos_precipitacion(
        latitud=LAT_OVALLE,
        longitud=LON_OVALLE,
        fecha_inicio=FECHA_INICIO,
        fecha_fin=FECHA_FIN
    )

    print("\nEstructura de la respuesta recibida:")
    print(f"Unidad de medida: {datos_crudos.get('daily_units', {}).get('precipitation_sum')}")
    print(f"Primeros 5 días: {datos_crudos.get('daily', {}).get('time', [])[:5]}")
    print(f"Milímetros caídos: {datos_crudos.get('daily', {}).get('precipitation_sum', [])[:5]}")