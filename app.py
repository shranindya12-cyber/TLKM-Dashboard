import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Dashboard Analisis Saham TLKM",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv("TLKM.csv")

forecast = pd.read_csv("forecast.csv")

# ======================================================
# PREPROCESSING
# ======================================================

df["date"] = pd.to_datetime(df["date"])

forecast["date"] = pd.to_datetime(
    forecast["date"]
)

# ======================================================
# SIDEBAR FILTER
# ======================================================

st.sidebar.title("Filter Dashboard")

periode = st.sidebar.selectbox(

    "Pilih Periode",

    [
        "7 Hari",
        "1 Bulan",
        "6 Bulan",
        "1 Tahun",
        "2 Tahun",
        "6 Tahun",
        "10 Tahun",
        "Max"
    ]
)

# ======================================================
# FILTER DATA
# ======================================================

today = df["date"].max()

if periode == "7 Hari":
    filtered_df = df[
        df["date"] >= today - pd.Timedelta(days=7)
    ]

elif periode == "1 Bulan":
    filtered_df = df[
        df["date"] >= today - pd.Timedelta(days=30)
    ]

elif periode == "6 Bulan":
    filtered_df = df[
        df["date"] >= today - pd.Timedelta(days=180)
    ]

elif periode == "1 Tahun":
    filtered_df = df[
        df["date"] >= today - pd.Timedelta(days=365)
    ]

elif periode == "2 Tahun":
    filtered_df = df[
        df["date"] >= today - pd.Timedelta(days=730)
    ]

elif periode == "6 Tahun":
    filtered_df = df[
        df["date"] >= today - pd.Timedelta(days=2190)
    ]

elif periode == "10 Tahun":
    filtered_df = df[
        df["date"] >= today - pd.Timedelta(days=3650)
    ]

else:
    filtered_df = df.copy()

# ======================================================
# HEADER
# ======================================================

st.title("Dashboard Analisis Saham TLKM")

st.caption(
    "Realtime Market Dashboard • Update Otomatis Setiap Hari Pukul 10.00 WIB"
)

# ======================================================
# LATEST PRICE
# ======================================================

latest_close = filtered_df["open"].iloc[-1]

previous_close = filtered_df["open"].iloc[-2]

price_change = (
    latest_close - previous_close
)

percent_change = (
    price_change / previous_close
) * 100

latest_volume = (
    filtered_df["volume"].iloc[-1]
)

# ======================================================
# METRICS
# ======================================================

col1, col2, col3 = st.columns(3)

col1.metric(

    "Latest Price",

    f"{latest_close:,.0f}",

    f"{price_change:,.0f} ({percent_change:.2f}%)"
)

col2.metric(

    "Volume",

    f"{latest_volume:,.0f}"
)

col3.metric(

    "Volatility",

    f"{filtered_df['volatility'].mean():.4f}"
)

# ======================================================
# STATISTIK
# ======================================================

st.subheader("Analisis Statistik")

stat1, stat2, stat3, stat4 = st.columns(4)

stat1.metric(

    "Average Open",

    round(
        filtered_df["open"].mean(),
        2
    )
)

stat2.metric(

    "Average Close",

    round(
        filtered_df["close"].mean(),
        2
    )
)

stat3.metric(

    "Highest Price",

    round(
        filtered_df["high"].max(),
        2
    )
)

stat4.metric(

    "Lowest Price",

    round(
        filtered_df["low"].min(),
        2
    )
)

# ======================================================
# MOVING AVERAGE
# ======================================================

filtered_df["MA7"] = (
    filtered_df["close"]
    .rolling(7)
    .mean()
)

filtered_df["MA30"] = (
    filtered_df["close"]
    .rolling(30)
    .mean()
)

# ======================================================
# HARGA SAHAM
# ======================================================

st.subheader("Pergerakan Harga Saham")

fig1 = go.Figure()

fig1.add_trace(

    go.Scatter(

        x=filtered_df["date"],

        y=filtered_df["close"],

        mode="lines",

        name="Harga"
    )
)

fig1.add_trace(

    go.Scatter(

        x=filtered_df["date"],

        y=filtered_df["MA7"],

        mode="lines",

        name="MA7"
    )
)

fig1.add_trace(

    go.Scatter(

        x=filtered_df["date"],

        y=filtered_df["MA30"],

        mode="lines",

        name="MA30"
    )
)

fig1.update_layout(

    height=500,

    template="plotly_dark"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================================================
# VOLUME
# ======================================================

st.subheader("Volume Trading")

fig2 = px.bar(

    filtered_df,

    x="date",

    y="volume"
)

fig2.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ======================================================
# VOLATILITY
# ======================================================

st.subheader("Analisis Volatilitas")

fig3 = px.line(

    filtered_df,

    x="date",

    y="volatility"
)

fig3.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ======================================================
# FORECAST
# ======================================================

st.subheader("Forecast 30 Hari (LSTM)")

fig4 = px.line(

    forecast,

    x="date",

    y="forecast"
)

fig4.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ======================================================
# LAST UPDATE
# ======================================================

st.caption(
    f"Last Updated : {today}"
)
