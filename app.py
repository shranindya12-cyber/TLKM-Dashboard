import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="TLKM Stock Dashboard",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv("TLKM.csv")
forecast = pd.read_csv("forecast.csv")

df["date"] = pd.to_datetime(df["date"])
forecast["date"] = pd.to_datetime(forecast["date"])

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("Filter")

periode = st.sidebar.selectbox(

    "Periode",

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
# FEATURE ENGINEERING
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
# HEADER
# ======================================================

st.title("Dashboard Analisis Saham TLKM")

st.caption(
    "Data diperbarui otomatis setiap hari pukul 10.00 WIB"
)

# ======================================================
# METRICS
# ======================================================

latest_close = filtered_df["close"].iloc[-1]
previous_close = filtered_df["close"].iloc[-2]

price_change = latest_close - previous_close

percent_change = (
    price_change / previous_close
) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest Price",
    f"Rp {latest_close:,.0f}",
    f"{price_change:,.0f} ({percent_change:.2f}%)"
)

col2.metric(
    "Average Open",
    f"Rp {filtered_df['open'].mean():,.0f}"
)

col3.metric(
    "Average Close",
    f"Rp {filtered_df['close'].mean():,.0f}"
)

col4.metric(
    "Volatility",
    f"{filtered_df['volatility'].mean():.4f}"
)

# ======================================================
# CHART HARGA
# ======================================================

st.subheader("Pergerakan Harga Saham")

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=filtered_df["date"],
        y=filtered_df["close"],
        name="Close",
        line=dict(width=3)
    )
)

fig1.add_trace(
    go.Scatter(
        x=filtered_df["date"],
        y=filtered_df["MA7"],
        name="MA7",
        line=dict(dash="dot")
    )
)

fig1.add_trace(
    go.Scatter(
        x=filtered_df["date"],
        y=filtered_df["MA30"],
        name="MA30",
        line=dict(dash="dash")
    )
)

fig1.update_layout(

    height=500,

    template="simple_white",

    legend=dict(
        orientation="h"
    ),

    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    )
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================================================
# ROW 2
# ======================================================

left, right = st.columns(2)

# ======================================================
# VOLUME
# ======================================================

with left:

    st.subheader("Volume Trading")

    fig2 = px.bar(

        filtered_df,

        x="date",

        y="volume"
    )

    fig2.update_layout(

        height=400,

        template="simple_white",

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ======================================================
# VOLATILITY
# ======================================================

with right:

    st.subheader("Analisis Volatilitas")

    fig3 = px.line(

        filtered_df,

        x="date",

        y="volatility"
    )

    fig3.update_layout(

        height=400,

        template="simple_white",

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ======================================================
# STATISTIK
# ======================================================

st.subheader("Analisis Statistik")

stats = pd.DataFrame({

    "Statistik": [

        "Highest Price",
        "Lowest Price",
        "Average Open",
        "Average Close",
        "Standard Deviation",
        "Average Return"
    ],

    "Nilai": [

        round(filtered_df["high"].max(),2),

        round(filtered_df["low"].min(),2),

        round(filtered_df["open"].mean(),2),

        round(filtered_df["close"].mean(),2),

        round(filtered_df["close"].std(),2),

        round(filtered_df["daily_return"].mean(),4)
    ]
})

st.dataframe(
    stats,
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

    height=500,

    template="simple_white",

    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    )
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ======================================================
# FOOTER
# ======================================================

st.caption(
    f"Last Updated : {today}"
)
