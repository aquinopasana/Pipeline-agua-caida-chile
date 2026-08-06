# 🌧️ Pipeline ETL de Precipitación Meteorológica (Open-Meteo & PostgreSQL)

Un pipeline de datos automatizado y contenerizado para la extracción, transformación y carga (ETL) de datos históricos de precipitación diaria (agua caída en `mm`) desde la API de **Open-Meteo**, almacenándolos en una base de datos relacional **PostgreSQL** mediante **Docker Compose** para su posterior consumo en herramientas de analítica como **Power BI**.

---

## 📐 Arquitectura del Pipeline

```text
  [ API Open-Meteo ] ──(HTTP GET / JSON)──> [ Python ETL Container ]
                                                   │
                                            (Pandas Transform)
                                                   │
                                            (SQLAlchemy / Load)
                                                   ▼
 [ Power BI / Dashboard ] <──(Port 5432)── [ PostgreSQL Container ]
![Dashboard de Power BI](imagenes/PBi agua caída.png)
