import pandas as pd
from load import obtener_motor_conexion


def consultar_precipitaciones():
    # Obtener el motor de conexión a PostgreSQL
    engine = obtener_motor_conexion()

    # Consulta SQL para traer todos los datos ordenados por fecha
    query = """
        SELECT fecha, localidad, precipitacion_mm, hubo_lluvia, mes, anio
        FROM precipitaciones_diarias
        ORDER BY fecha DESC;
    """

    # Cargar el resultado directamente a un DataFrame de Pandas
    df_resultado = pd.read_sql(query, con=engine)

    print(f"\n--- Registros Totales en la Base de Datos: {len(df_resultado)} ---")
    print(df_resultado.head(15))  # Muestra los últimos 15 días guardados

    # Consulta de agregación: Total de agua caída en la localidad
    query_total = """
        SELECT 
            localidad, 
            SUM(precipitacion_mm) as total_agua_caida_mm,
            COUNT(*) FILTER (WHERE hubo_lluvia = true) as dias_con_lluvia
        FROM precipitaciones_diarias
        GROUP BY localidad;
    """
    df_resumen = pd.read_sql(query_total, con=engine)

    print("\n--- Resumen de Agua Caída (mm) ---")
    print(df_resumen)


if __name__ == "__main__":
    consultar_precipitaciones()