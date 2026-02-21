import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Behavioral Risk Radar",
    layout="wide"
)

# -----------------------------
# Sidebar - Portfolio Builder
# -----------------------------

st.sidebar.title("📊 Portfolio Builder")

available_assets = ["AAPL", "MSFT", "SPY", "QQQ", "XLF", "GLD"]

selected_assets = st.sidebar.multiselect(
    "Select Assets",
    available_assets,
    default=["AAPL", "SPY"]
)

weights = {}

if selected_assets:
    st.sidebar.markdown("### Allocation Weights")
    total_weight = 0

    for asset in selected_assets:
        weight = st.sidebar.slider(
            f"{asset} Weight (%)",
            min_value=0,
            max_value=100,
            value=int(100 / len(selected_assets))
        )
        weights[asset] = weight
        total_weight += weight

    st.sidebar.markdown(f"**Total Allocation: {total_weight}%**")

    if total_weight != 100:
        st.sidebar.warning("⚠️ Total weight must equal 100%")

# -----------------------------
# Main Title
# -----------------------------

st.title("🧠 Behavioral Risk Radar")
st.markdown(
    "AI-powered behavioral risk profiling and stress testing for retail investors."
)

# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    ["📁 Portfolio Overview", "📈 Risk Radar", "🔥 Stress Test", "🤖 AI Insights"]
)

# -----------------------------
# Tab 1 - Portfolio Overview
# -----------------------------

with tab1:
    st.header("Portfolio Snapshot")

    col1, col2, col3 = st.columns(3)

    col1.metric("Portfolio Volatility", "15.2%")
    col2.metric("Concentration Index", "0.28")
    col3.metric("Behavior Cluster", "Diversified Investor")

    if selected_assets:
        df = pd.DataFrame({
            "Asset": list(weights.keys()),
            "Weight": list(weights.values())
        })

        fig = px.pie(df, names="Asset", values="Weight", title="Allocation Breakdown")
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 2 - Risk Radar
# -----------------------------

with tab2:
    st.header("Risk Radar")

    radar_data = pd.DataFrame({
        "Metric": ["Volatility", "Concentration", "Correlation", "Sector Risk"],
        "Score": [0.6, 0.4, 0.5, 0.7]
    })

    fig = px.line_polar(
        radar_data,
        r="Score",
        theta="Metric",
        line_close=True
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 3 - Stress Test
# -----------------------------

with tab3:
    st.header("Monte Carlo Stress Simulation")

    horizon = st.slider("Time Horizon (Days)", 30, 365, 180)
    confidence = st.slider("Confidence Level (%)", 90, 99, 95)

    st.metric("Estimated VaR", "-12.4%")
    st.metric("Expected Shortfall", "-18.7%")

    simulated_returns = np.random.normal(-0.05, 0.1, 1000)

    fig = px.histogram(simulated_returns, nbins=40)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 4 - AI Insights
# -----------------------------

with tab4:
    st.header("Behavioral Profile")

    st.success("You are classified as a Diversified Long-Term Investor.")

    st.markdown("""
    ### Key Observations:
    - Moderate volatility exposure
    - Healthy diversification
    - Limited sector concentration
    
    ### Recommendations:
    - Consider reducing correlation between equity holdings
    - Increase allocation to defensive assets during volatile periods
    """)