import streamlit as st
import pandas as pd
import plotly.express as px
from Proyecto_Final import read_table_sql


# diccionario de paises

paises_dict = {
    "MX": "México",
    "US": "Estados Unidos",
    "CA": "Canadá",
    "ES": "España",
    "BR": "Brasil",
    "AR": "Argentina",
    "CL": "Chile",
    "CO": "Colombia",
    "PE": "Perú",
    "JP": "Japón",
    "KR": "Corea del Sur",
    "GB": "Reino Unido",
    "DE": "Alemania",
    "FR": "Francia",
    "IT": "Italia"
}


# funcion para cargar PIB
def cargar_pib(codigo):
    df = read_table_sql(f"{codigo}_NY_GDP_MKTP_KD_ZG")
    if df is None or df.empty:
        return None
    df = df.rename(columns={"date": "Year", "Value": "PIB"})
    df["Year"] = df["Year"].astype(int)
    df["PIB"] = df["PIB"].astype(float)
    df = df.sort_values("Year")
    return df



# cargar todos los paises en un diccionario

data_pib = {}
for code, name in paises_dict.items():
    df_tmp = cargar_pib(code)
    if df_tmp is not None:
        df_tmp["País"] = name
        data_pib[name] = df_tmp


(tab3,) = st.tabs(["🌎 PIB Internacional"])

with tab3:

    st.subheader("🌍 Comparación Internacional del Crecimiento del PIB ")
    # validamos que hayan cargado
    if not data_pib:
        st.error("No se pudieron obtener datos del PIB desde SQL Server")
        st.stop()


    paises_seleccion = st.multiselect(
        "Elige uno o varios países:",
        list(data_pib.keys()),
        default=["México", "Estados Unidos"]
    )

    if not paises_seleccion:
        st.warning("Selecciona al menos un país para visualizar datos.")
        st.stop()

    # concatenar los df seleccionados
    df_all = pd.concat([data_pib[p] for p in paises_seleccion], ignore_index=True)


    # rango dinamico de años
    min_year, max_year = df_all["Year"].min(), df_all["Year"].max()

    año_min, año_max = st.slider(
        "📅 Rango de años a visualizar",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year))
    )

    df_filtered = df_all[(df_all["Year"] >= año_min) & (df_all["Year"] <= año_max)]


    # KPIs
    st.subheader("📊 Indicadores clave del PIB")

    cols = st.columns(len(paises_seleccion))

    for i, pais in enumerate(paises_seleccion):
        df = data_pib[pais]

        if len(df) >= 2:
            ult = df.iloc[-1]["PIB"]
            ant = df.iloc[-2]["PIB"]
        else:
            ult, ant = 0, 0

        cols[i].metric(
            label=f"{pais} – PIB actual",
            value=f"{ult:.2f}%",
            delta=f"{ult - ant:.2f}%"
        )


    # comparacion historica (tabla pivote)
    st.subheader("📋 Comparación histórica (últimos 15 años)")

    tabla = df_filtered.pivot(index="Year", columns="País", values="PIB")
    tabla = tabla.sort_index(ascending=False).head(15).sort_index()

    st.dataframe(tabla, use_container_width=True)


    #linea historica
    st.subheader("📉 Tendencia del crecimiento del PIB")

    fig_line = px.line(
        df_filtered,
        x="Year",
        y="PIB",
        color="País",
        markers=True,
        title="Tendencia del Crecimiento Económico"
    )
    fig_line.update_traces(line_width=3)
    st.plotly_chart(fig_line, use_container_width=True)



    # barras del ultimo dato disponible por pais
    st.subheader("🏁 Último dato disponible por país")

    ultimos = df_filtered.sort_values("Year").groupby("País").tail(1)

    fig_bar = px.bar(
        ultimos,
        x="País",
        y="PIB",
        text="PIB",
        title="Crecimiento del PIB – Último Año Disponible"
    )
    fig_bar.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)


    # ranking en tabla para los paises (es del ultimo año)
    st.subheader("🏆 Ranking de crecimiento del PIB")

    ranking = ultimos.sort_values("PIB", ascending=False)[["País", "PIB"]]
    st.table(ranking)
