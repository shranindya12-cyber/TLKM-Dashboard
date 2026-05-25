

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="TLKM Dashboard",
    layout="wide"
)

df = pd.read_csv("TLKM.csv")

forecast = pd.read_csv("forecast.csv")

summary = pd.read_csv(
    "summary_stats.csv"
)

st.title("Dashboard Saham TLKM")

st.caption(
    "Data diperbarui otomatis setiap hari pukul 10.00 WIB"
)

last_update = df["date"].iloc[-1]

st.write(
    f"Last Updated: {last_update}"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest Price",
    round(df["close"].iloc[-1],2)
)

col2.metric(
    "Highest Price",
    round(df["close"].max(),2)
)

col3.metric(
    "Lowest Price",
    round(df["close"].min(),2)
)

col4.metric(
    "Volatility",
    round(df["volatility"].mean(),4)
)

st.subheader(
    "Trend Harga Saham"
)

fig1 = px.line(

    df.tail(365),

    x="date",

    y=[
        "close",
        "MA20",
        "MA50",
        "MA200"
    ]
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader(
    "Volume Transaksi"
)

fig2 = px.bar(

    df.tail(365),

    x="date",

    y="volume"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader(
    "Rolling Volatility"
)

fig3 = px.line(

    df.tail(365),

    x="date",

    y="volatility"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.subheader(
    "Forecast 30 Hari"
)

fig4 = px.line(

    forecast,

    x="date",

    y="forecast"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

