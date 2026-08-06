import sys
from datetime import datetime
from extract import extraer_datos_precipitacion
from transform import transformar_datos_precipitacion
from load import cargar_dataframe_a_postgres


def ejecutar_pipeline_clima(
    latitud: float,
    longitud: float,
    nombre_localidad: str,
    fecha_inicio: str,
    fecha_fin: str,
    nombre_tabla: str = "precipitaciones_diarias"
):
    """
    Orquesta la ejecución completa del pipeline ETL de precipitaciones.
    """
    print("\n" + "="*50)
    print(f"🚀 INICIANDO PIPELINE ETL: {nombre_localidad.upper()}")
    print(f"   Rango: {fecha_inicio} a {fecha_fin}")
    print("="*50)

    try:
        # 1. ETAPA DE EXTRACCIÓN (E)
        print("\n[1/3] 📡 Extrayendo datos de la API Open-Meteo...")
        datos_crudos = extraer_datos_precipitacion(
            latitud=latitud,
            longitud=longitud,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        # 2. ETAPA DE TRANSFORMACIÓN (T)
        print("\n[2/3] ⚙️ Transformando datos con Pandas...")
        df_clima = transformar_datos_precipitacion(
            datos_json=datos_crudos,
            nombre_localidad=nombre_localidad
        )
        print(f"   -> Se procesaron {len(df_clima)} registros diarios.")

        # 3. ETAPA DE CARGA (L)
        print("\n[3/3] 💾 Cargando datos en PostgreSQL...")
        exito = cargar_dataframe_a_postgres(
            df=df_clima,
            nombre_tabla=nombre_tabla
        )

        if exito:
            print("\n" + "="*50)
            print("✅ PIPELINE COMPLETADO CON ÉXITO")
            print("="*50 + "\n")

    except Exception as error:
        print("\n" + "❌"*25)
        print(f"FALLO EN EL PIPELINE: {error}")
        print("❌"*25 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    # Parametrización del Pipeline (Coordenadas de Ovalle, Coquimbo)
    LATITUD_OVALLE = -30.5983
    LONGITUD_OVALLE = -71.2003
    LOCALIDAD = "Ovalle"

    # Definir el rango de fechas (ej: todo el mes de julio de 2026)
    FECHA_INICIO = "2026-07-01"
    FECHA_FIN = "2026-07-31"

    # Nombre de la tabla destino en PostgreSQL
    TABLA_DESTINO = "precipitaciones_diarias"

    # Ejecución
    ejecutar_pipeline_clima(
        latitud=LATITUD_OVALLE,
        longitud=LONGITUD_OVALLE,
        nombre_localidad=LOCALIDAD,
        fecha_inicio=FECHA_INICIO,
        fecha_fin=FECHA_FIN,
        nombre_tabla=TABLA_DESTINO
    )