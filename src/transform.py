import pandas as pd


def transformar_datos_precipitacion(datos_json: dict, nombre_localidad: str = "Ovalle") -> pd.DataFrame:
    """
    Toma la respuesta JSON de la API de Open-Meteo y la transforma en un 
    DataFrame de Pandas limpio y estructurado para guardar en la base de datos.

    Parámetros:
      - datos_json (dict): Diccionario devuelto por extract.py
      - nombre_localidad (str): Nombre de la ubicación para identificar los registros.

    Retorna:
      - pd.DataFrame: Tabla procesada con tipos de datos correctos.
    """
    if not datos_json or "daily" not in datos_json:
        raise ValueError("El JSON recibido no contiene la clave 'daily' con los datos requeridos.")

    # 1. Extraer las listas de fechas y precipitaciones del JSON
    fechas = datos_json["daily"].get("time", [])
    precipitaciones = datos_json["daily"].get("precipitation_sum", [])
    latitud = datos_json.get("latitude")
    longitud = datos_json.get("longitude")

    # 2. Construir el DataFrame de Pandas
    df = pd.DataFrame({
        "fecha": fechas,
        "precipitacion_mm": precipitaciones
    })

    # 3. Transformaciones y Limpieza de Datos
    
    # Convertir la columna 'fecha' a tipo datetime
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Asegurar que la precipitación sea de tipo flotante
    df["precipitacion_mm"] = df["precipitacion_mm"].astype(float)

    # Reemplazar valores nulos (NaN) por 0.0 mm si los hubiera
    df["precipitacion_mm"] = df["precipitacion_mm"].fillna(0.0)

    # 4. Agregar Metadatos útiles para la Base de Datos y Power BI
    df["localidad"] = nombre_localidad
    df["latitud"] = latitud
    df["longitud"] = longitud
    
    # Crear columnas calculadas convenientes para Power BI (Año, Mes, Día de la semana)
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    # ✅ SOLUCIÓN ROBUSTA (sin dependencia del sistema operativo):
    dias_espaniol = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
}

    df["dia_nombre"] = df["fecha"].dt.day_name().map(dias_espaniol)
    # df["dia_nombre"] = df["fecha"].dt.day_name(locale="es_ES")  # Ej: Lunes, Martes
    df["hubo_lluvia"] = df["precipitacion_mm"] > 0.0  # Booleano True/False

    # Reordenar las columnas en una estructura clara
    columnas_ordenadas = [
        "fecha", "localidad", "precipitacion_mm", "hubo_lluvia",
        "anio", "mes", "dia_nombre", "latitud", "longitud"
    ]
    df = df[columnas_ordenadas]

    return df


# Bloque de prueba local combinando Extract + Transform
if __name__ == "__main__":
    from extract import extraer_datos_precipitacion

    print("--- Probando Pipeline: Extract -> Transform ---")
    
    # 1. Ejecutar Extracción
    LAT_OVALLE = -30.5983
    LON_OVALLE = -71.2003
    
    datos_crudos = extraer_datos_precipitacion(
        latitud=LAT_OVALLE,
        longitud=LON_OVALLE,
        fecha_inicio="2026-07-01",
        fecha_fin="2026-07-31"
    )

    # 2. Ejecutar Transformación
    df_clima = transformar_datos_precipitacion(datos_crudos, nombre_localidad="Ovalle")

    print("\n--- Resultado del DataFrame Transformado ---")
    print(df_clima.info())
    print("\nPrimeras 5 filas:")
    print(df_clima.head())
    
    print("\nResumen estadístico de agua caída (mm):")
    print(df_clima["precipitacion_mm"].describe())

    # --- COLOCAR AL FINAL DE src/transform.py ---

if __name__ == "__main__":
    from extract import extraer_datos_precipitacion

    print("\n1. Iniciando Extracción de prueba...")
    
    # Coordenadas de Ovalle
    LAT_OVALLE = -30.5983
    LON_OVALLE = -71.2003
    
    # Rango de fechas recientes (junio 2026)
    FECHA_INICIO = "2026-07-15"
    FECHA_FIN = "2026-07-25"

    try:
        # 1. Obtener datos crudos
        datos_crudos = extraer_datos_precipitacion(
            latitud=LAT_OVALLE,
            longitud=LON_OVALLE,
            fecha_inicio=FECHA_INICIO,
            fecha_fin=FECHA_FIN
        )

        print("\n2. Iniciando Transformación a DataFrame...")
        # 2. Transformar
        df_clima = transformar_datos_precipitacion(datos_crudos, nombre_localidad="Ovalle")

        print("\n================ RESULTADO DEL DATAFRAME ================")
        print(df_clima.head(10))  # Muestra las primeras 10 filas
        print("=========================================================\n")

    except Exception as e:
        print(f"\n❌ Ocurrió un error durante la prueba: {e}")