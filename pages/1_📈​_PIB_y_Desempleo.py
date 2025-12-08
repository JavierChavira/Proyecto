import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from Proyecto_Final import read_table_sql



# Cargar tablas
df_gdp = read_table_sql("MX_NY_GDP_MKTP_KD_ZG")
df_unem = read_table_sql("MX_SL_UEM_TOTL_ZS")

(tab1,) = st.tabs(["🇲🇽 PIB y Desempleo"])

with tab1:

    st.subheader("📈 Desempeño Económico de México: PIB y Desempleo")

    # Validación
    if df_gdp is None or df_unem is None or df_gdp.empty or df_unem.empty:
        st.error("Error cargando tablas desde SQL.")
        st.stop()

    # limpieza y union
    df_gdp = df_gdp.rename(columns={"date": "Year", "PIB": "PIB"})
    df_unem = df_unem.rename(columns={"date": "Year", "Desempleo": "Desempleo"})

    # convertimos year a entero
    df_gdp["Year"] = df_gdp["Year"].astype(int)
    df_unem["Year"] = df_unem["Year"].astype(int)

    # unimos
    df = pd.merge(df_gdp, df_unem, on="Year", how="inner").sort_values("Year")


    # slider
    min_year, max_year = df["Year"].min(), df["Year"].max()

    rango = st.slider(
        "📅 Selecciona el rango de años:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # filtrar
    filtered = df[(df["Year"] >= rango[0]) & (df["Year"] <= rango[1])]

    ultimo = filtered.iloc[-1]
    penultimo = filtered.iloc[-2]

    # metricas
    st.markdown("### 🧮 Indicadores Clave (México)")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "🇲🇽 PIB Actual",
        f"{ultimo['PIB']:.2f}%",
        f"{ultimo['PIB'] - penultimo['PIB']:.2f}%"
    )

    k2.metric(
        "💼 Desempleo Actual",
        f"{ultimo['Desempleo']:.2f}%",
        f"{ultimo['Desempleo'] - penultimo['Desempleo']:.2f}%"
    )

    # promedios últimos 5 años
    promedio_pib = filtered.tail(5)["PIB"].mean()
    promedio_des = filtered.tail(5)["Desempleo"].mean()

    k3.metric("📌 PIB Promedio 5 años", f"{promedio_pib:.2f}%")
    k4.metric("📌 Desempleo Promedio 5 años", f"{promedio_des:.2f}%")

    st.markdown("---")

    # grafico combinado pib y desempleo
    st.markdown("### 📊 Tendencias históricas: PIB vs Desempleo")

    fig_combo = go.Figure()

    fig_combo.add_trace(go.Scatter(
        x=filtered["Year"], y=filtered["PIB"],
        name="PIB (%)", mode="lines+markers"
    ))

    fig_combo.add_trace(go.Scatter(
        x=filtered["Year"], y=filtered["Desempleo"],
        name="Desempleo (%)", mode="lines+markers",
        yaxis="y2"
    ))

    fig_combo.update_layout(
        title="PIB vs Desempleo (Doble Eje)",
        yaxis=dict(title="PIB (%)"),
        yaxis2=dict(title="Desempleo (%)", overlaying="y", side="right"),
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig_combo, use_container_width=True)

    st.markdown("---")

    # insights
    st.markdown("### 🔎 Insights Rápidos")

    c1, c2, c3 = st.columns(3)

    ultimos8 = filtered.tail(8)

    # Barra de PIB
    with c1:
        fig_pib_last = px.bar(
            ultimos8, x="Year", y="PIB",
            title="📊 PIB: Últimos 8 Años",
            text="PIB"
        )
        fig_pib_last.update_traces(texttemplate='%{text:.2f}%')
        st.plotly_chart(fig_pib_last, use_container_width=True)

    # Barra de desempleo
    with c2:
        fig_unem_last = px.bar(
            ultimos8, x="Year", y="Desempleo",
            title="💼 Desempleo: Últimos 8 Años",
            text="Desempleo"
        )
        fig_unem_last.update_traces(texttemplate='%{text:.2f}%')
        st.plotly_chart(fig_unem_last, use_container_width=True)

    # Pie
    with c3:
        fig_pie = px.pie(
            names=["PIB Medio", "Desempleo Medio"],
            values=[promedio_pib, promedio_des],
            title="⚖️ Relación PIB - Desempleo (promedios recientes)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # una tabla historica completa
    st.markdown("### 📋 Tabla histórica")
    st.dataframe(filtered, use_container_width=True, height=300)

    # resumen
    st.markdown("### 📝 Resumen de los datos")

    cambio_pib = ultimo["PIB"] - penultimo["PIB"]
    cambio_des = ultimo["Desempleo"] - penultimo["Desempleo"]

    st.info(
        f"• El PIB más reciente es **{ultimo['PIB']:.2f}%**, variando **{cambio_pib:.2f}%**.\n"
        f"• El desempleo actual es **{ultimo['Desempleo']:.2f}%**, cambiando **{cambio_des:.2f}%**.\n"
        f"• Promedio reciente del PIB: **{promedio_pib:.2f}%**.\n"
        f"• Promedio reciente del desempleo: **{promedio_des:.2f}%**."
    )
