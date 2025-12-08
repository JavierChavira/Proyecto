import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import sys

#conexion a SQL server
def conectar():
    server = r"Usuario\SQLEXPRESS"
    database = "Proyecto"
    driver = "ODBC+Driver+17+for+SQL+Server"

    cadena = f"mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes"

    return create_engine(cadena).connect()


#esta funcion construye la URL, hace peticion http, verifica que la api respondio,
#Convierte la respuesta en JSON, de ahi limpia los datos porque la api da varios nulos
#y devuelve el dataframe ya limpio
def get_indicator(country, indicator, name):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=2000"
    r = requests.get(url)

    if r.status_code != 200:
        return pd.DataFrame()

    data = r.json()
    if len(data) < 2:
        return pd.DataFrame()

    cleaned = []
    for item in data[1]:
        if item["value"] is not None:
            cleaned.append({
                "date": int(item["date"]),
                name: float(item["value"])
            })

    return pd.DataFrame(cleaned).sort_values("date")

#llama a la funcion get_indicator() para obtener limpio el DataFrame,
#si viene vacio muestra error, conecta a SQL Server, construye el nombre de la tabla,
#guarda el DataFrame en SQL ya listo para que podamos usarlo en las visualizaciones
def save_indicator_to_sql(country, indicator, column_name):
    df = get_indicator(country, indicator, column_name)

    if df.empty:
        print(f" No se pudo obtener {indicator} de {country}")
        return

    engine = conectar()
    table_name = f"{country}_{indicator}".replace(".", "_")

    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Tabla creada: {table_name}")





def read_table_sql(table_name):
    engine = conectar()
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)



def portada():
    st.set_page_config(page_title="Portada - Proyecto Final", layout="wide")
    st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 46px;
        font-weight: bold;
        margin-top: -30px;
    }
    .name-box {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    .desc-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        font-size: 18px;
        text-align: justify;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        color: black;
    }
        .desc-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        font-size: 18px;
        text-align: justify;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='title'>Proyecto Final – Programación para la Extracción de Datos</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("***Integrantes***")

    st.write("")

    col1, col2, col3, col4, col5,col6 = st.columns(6)

    imagenes = ["Foto1.jpg", "Foto2.jpg", "Foto3.jpg", "Foto4.jpg", "Foto5.jpg","Foto6.jpg"]
    nombres = [
        "Mora Villanueva Marco Antonio",
        "Contreras Nevarez Carlos Manuel",
        "Rodriguez Chavira Francisco Javier",
        "Velazquez Ruiz Leonardo",
        "Longoria Mendoza Sergio Luis",
        "Victor Miguel Hernandez Rodriguez"
    ]

    columnas = [col1, col2, col3, col4, col5, col6]

    for col, img, nombre in zip(columnas, imagenes, nombres):
        with col:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.image(img, width=300)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(f"<p class='name-box'>{nombre}</p>", unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("***Descripción del proyecto***")
    st.write(
        """
        <div class='desc-box'>
        Este proyecto tiene como objetivo integrar herramientas de extracción, transformación y visualización de datos 
        utilizando Python, Streamlit, SQL Server y APIs públicas del Banco Mundial. El sistema permite consultar 
        indicadores económicos clave, almacenarlos en una base de datos, analizarlos y presentarlos mediante dashboards 
        interactivos que facilitan su interpretación para la toma de decisiones.  
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.subheader("***Link del GitHub***")
    st.write(
        """
        <div class='desc-box'>
        https://github.com/JavierChavira/Proyecto
        </div>
        """,unsafe_allow_html=True)




if __name__ == "__main__":

    if "--update" in sys.argv:
        print("actualizando...")
        # México
        save_indicator_to_sql("MX", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("MX", "SL.UEM.TOTL.ZS", "Desempleo")
        save_indicator_to_sql("MX", "FP.CPI.TOTL.ZG", "Inflación")

        # Estados Unidos
        save_indicator_to_sql("US", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("US", "FP.CPI.TOTL.ZG", "Inflación")

        # Canada
        save_indicator_to_sql("CA", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("CA", "FP.CPI.TOTL.ZG", "Inflación")

        # Espana
        save_indicator_to_sql("ES", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("ES", "FP.CPI.TOTL.ZG", "Inflación")

        # Brasil
        save_indicator_to_sql("BR", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("BR", "FP.CPI.TOTL.ZG", "Inflación")

        # Argentina
        save_indicator_to_sql("AR", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("AR", "FP.CPI.TOTL.ZG", "Inflación")

        # Chile
        save_indicator_to_sql("CL", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("CL", "FP.CPI.TOTL.ZG", "Inflación")

        # Colombia
        save_indicator_to_sql("CO", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("CO", "FP.CPI.TOTL.ZG", "Inflación")

        # Perú
        save_indicator_to_sql("PE", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("PE", "FP.CPI.TOTL.ZG", "Inflación")

        # Japón
        save_indicator_to_sql("JP", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("JP", "FP.CPI.TOTL.ZG", "Inflación")

        # Corea del Sur
        save_indicator_to_sql("KR", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("KR", "FP.CPI.TOTL.ZG", "Inflación")

        # Reino Unido
        save_indicator_to_sql("GB", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("GB", "FP.CPI.TOTL.ZG", "Inflación")

        # Alemania
        save_indicator_to_sql("DE", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("DE", "FP.CPI.TOTL.ZG", "Inflación")

        # Francia
        save_indicator_to_sql("FR", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("FR", "FP.CPI.TOTL.ZG", "Inflación")

        # Italia
        save_indicator_to_sql("IT", "NY.GDP.MKTP.KD.ZG", "PIB")
        save_indicator_to_sql("IT", "FP.CPI.TOTL.ZG", "Inflación")
    else:
        portada()




