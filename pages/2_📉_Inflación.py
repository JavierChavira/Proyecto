import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
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

# carga las tablas de inflacion
df_list = []

for code, nombre in paises_dict.items():
    try:
        df = read_table_sql(f"{code}_FP_CPI_TOTL_ZG")
        df["País"] = nombre
        df_list.append(df)
    except:
        pass  # Ignorar si un país no tiene datos

# unificar
df_all = pd.concat(df_list, ignore_index=True)
df_all["date"] = df_all["date"].astype(int)
df_all["Inflación"] = df_all["Inflación"].astype(float)
df_all = df_all.sort_values("date")

# ================================================================
(tab2,) = st.tabs(["📉 Inflación"])
# ================================================================

with tab2:

    st.subheader("📈 Inflación en México y Comparativa Internacional ")
    st.markdown("---")

    # SLIDER

    min_year, max_year = int(df_all["date"].min()), int(df_all["date"].max())

    año_min, año_max = st.slider(
        "📅 Selecciona el rango de años a visualizar",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    df_filtered = df_all[
        (df_all["date"] >= año_min) & (df_all["date"] <= año_max)
        ]

    st.markdown("---")

    # metricas de mexico
    df_mex = df_filtered[df_filtered["País"] == "México"]

    col1, col2, col3 = st.columns(3)

    if len(df_mex) >= 2:
        ultimo = df_mex.iloc[-1]
        penultimo = df_mex.iloc[-2]

        col1.metric(
            "🔥 Inflación actual en México",
            f"{ultimo['Inflación']:.2f}%",
            f"{ultimo['Inflación'] - penultimo['Inflación']:.2f}%"
        )

        col2.metric(
            "📊 Promedio histórico",
            f"{df_mex['Inflación'].mean():.2f}%"
        )

        max_row = df_mex.loc[df_mex["Inflación"].idxmax()]
        col3.metric(
            "📈 Máxima registrada",
            f"{max_row['Inflación']:.2f}%",
            int(max_row["date"])
        )

    st.markdown("---")


    # comparamos a mexico contra otros paises para analizarlos
    st.subheader("🇲🇽 Compararacion de México contra otro país")

    paises_disponibles = [p for p in paises_dict.values() if p != "México"]

    pais_seleccionado = st.selectbox(
        "Selecciona un país para comparar:",
        paises_disponibles
    )

    df_compare = df_filtered[
        df_filtered["País"].isin(["México", pais_seleccionado])
    ]

    fig_comp = px.line(
        df_compare,
        x="date",
        y="Inflación",
        color="País",
        markers=True,
        title=f"📊 Comparación: México vs {pais_seleccionado}",
        template="plotly_white"
    )
    fig_comp.update_traces(line_width=3)
    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("---")

    st.subheader(f"📋 Comparación histórica: México vs {pais_seleccionado}")

    df_comp_table = df_compare.pivot(index="date", columns="País", values="Inflación")

    st.dataframe(df_comp_table, use_container_width=True)

    st.markdown("---")

    st.subheader("⚡ Insights de inflación en México")

    col1, col2, col3 = st.columns(3)

    # tendencia del último año
    tendencia = ultimo["Inflación"] - penultimo["Inflación"]
    col1.metric("📈 Variación anual", f"{tendencia:.2f}%")

    # promedio últimos 10 años
    prom_10 = df_mex.tail(10)["Inflación"].mean()
    col2.metric("📊 Promedio últimos 10 años", f"{prom_10:.2f}%")

    # dirección de los resultados
    dif_serie = df_mex["Inflación"].diff().dropna()
    racha = "🔥 Subiendo" if dif_serie.tail(3).mean() > 0 else "❄️ Bajando"
    col3.metric("📉 Tendencia reciente", racha)

    st.markdown("---")

    st.subheader("📊 Inflación más reciente por país")

    # obtener ultimo dato por país
    df_last = (
        df_filtered.sort_values("date").groupby("País").tail(1)
    )

    # selector de paises para la grafica
    paises_disponibles_barras = sorted(df_last["País"].unique())
    paises_seleccionados_barras = st.multiselect(
        "Selecciona los países a mostrar:",
        options=paises_disponibles_barras,
        default=paises_disponibles_barras  # Mostrar todos por defecto
    )

    # filtrar paises solo los elegidos
    df_last_filtrado = df_last[df_last["País"].isin(paises_seleccionados_barras)]

    # grafica
    fig_barras = px.bar(
        df_last_filtrado,
        x="País",
        y="Inflación",
        text="Inflación",
        title="Inflación actual (último año disponible)",
        template="plotly_white"
    )

    fig_barras.update_traces(
        texttemplate='%{text:.2f}%',
        textposition='outside'
    )

    st.plotly_chart(fig_barras, use_container_width=True)
