import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="TLKM Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.main {
    background-color: #081028;
}

[data-testid="stSidebar"] {
    background-color: #0E1726;
}

h1, h2, h3, h4 {
    color: white;
}

.metric-card {
    background: linear-gradient(
        145deg,
        #111827,
        #1F2937
    );

    padding: 20px;
    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.metric-title {
    font-size: 14px;
    color: #9CA3AF;
}

.metric-value {
    font-size: 34px;
    font-weight: bold;
    color: white;
}

.metric-change-up {
    color: #22C55E;
    font-size: 16px;
}

.metric-change-down {
    color: #EF4444;
    font-size: 16px;
}

.section-card {

    background: #111827;

    padding: 25px;

    border-radius: 18px;

    margin-top: 20px;

    border: 1px solid rgba(255,255,255,0.06);
}

.small-text {
    color: #9CA3AF;
}

</style>
""", unsafe_allow_html=True)

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

st.sidebar.title("📊 Dashboard Settings")

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

st.markdown("""
<h1 style='font-size:42px;'>
📈 TLKM Stock Analytics Dashboard
</h1>
<p class='small-text'>
Realtime Market Intelligence • Auto Update 10:00 WIB
</p>
""", unsafe_allow_html=True)

# ======================================================
# METRICS
# ======================================================

latest_close = filtered_df["close"].iloc[-1]
previous_close = filtered_df["close"].iloc[-2]

price_change = latest_close - previous_close
percent_change = (
    price_change / previous_close
) * 100

volume = filtered_df["volume"].iloc[-1]
volatility = filtered_df["volatility"].mean()

col1, col2, col3, col4 = st.columns(4)

# ======================================================
# CARD 1
# ======================================================

change_class = (
    "metric-change-up"
    if percent_change >= 0
    else "metric-change-down"
)

col1.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Latest Price
</div>

<div class="metric-value">
Rp {latest_close:,.0f}
</div>

<div class="{change_class}">
{price_change:,.0f}
({percent_change:.2f}%)
</div>

</div>
""", unsafe_allow_html=True)

# ======================================================
# CARD 2
# ======================================================

col2.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Trading Volume
</div>

<div class="metric-value">
{volume:,.0f}
</div>

<div class="small-text">
Latest Market Activity
</div>

</div>
""", unsafe_allow_html=True)

# ======================================================
# CARD 3
# ======================================================

col3.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Average Volatility
</div>

<div class="metric-value">
{volatility:.4f}
</div>

<div class="small-text">
Rolling Volatility
</div>

</div>
""", unsafe_allow_html=True)

# ======================================================
# CARD 4
# ======================================================

col4.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Highest Price
</div>

<div class="metric-value">
Rp {filtered_df['high'].max():,.0f}
</div>

<div class="small-text">
Selected Period
</div>

</div>
""", unsafe_allow_html=True)

# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3, tab4 = st.tabs([

    "📈 Trend",

    "📊 Statistics",

    "⚡ Volatility",

    "🔮 Forecast"
])

# ======================================================
# TAB 1
# ======================================================

with tab1:

    st.markdown("## Trend Analysis")

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["close"],
            mode="lines",
            name="Close Price",
            line=dict(width=3)
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

        template="plotly_dark",

        height=600,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ======================================================
# TAB 2
# ======================================================

with tab2:

    st.markdown("## Statistical Analysis")

    stats = pd.DataFrame({

        "Metric": [

            "Average Open",
            "Average Close",
            "Highest High",
            "Lowest Low",
            "Std Dev Close",
            "Mean Return"
        ],

        "Value": [

            round(filtered_df["open"].mean(),2),

            round(filtered_df["close"].mean(),2),

            round(filtered_df["high"].max(),2),

            round(filtered_df["low"].min(),2),

            round(filtered_df["close"].std(),2),

            round(filtered_df["daily_return"].mean(),4)
        ]
    })

    st.dataframe(
        stats,
        use_container_width=True
    )

# ======================================================
# TAB 3
# ======================================================

with tab3:

    st.markdown("## Volatility Analysis")

    fig2 = px.line(

        filtered_df,

        x="date",

        y="volatility"
    )

    fig2.update_layout(

        template="plotly_dark",

        height=500,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ======================================================
# TAB 4
# ======================================================

with tab4:

    st.markdown("## Forecasting (LSTM)")

    fig3 = px.line(

        forecast,

        x="date",

        y="forecast"
    )

    fig3.update_layout(

        template="plotly_dark",

        height=500,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    f"Last Updated : {today}"
)
