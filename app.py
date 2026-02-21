import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from model.predict_cluster import predict_behavior_cluster
from utils.simulation import run_monte_carlo_simulation, compute_var_es
from utils.interpretation import generate_behavior_insight

from utils.risk_metrics import (
    load_price_data,
    compute_daily_returns,
    compute_portfolio_volatility,
    compute_hhi,
    compute_correlation_exposure
)

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
    
    prices = load_price_data()
    returns = compute_daily_returns(prices)

    portfolio_vol = compute_portfolio_volatility(weights, returns)
    hhi = compute_hhi(weights)
    corr_exposure = compute_correlation_exposure(weights, returns)

    cluster_id = predict_behavior_cluster(hhi, portfolio_vol, corr_exposure)

cluster_labels = {
    0: "Diversified Long-Term Investor",
    1: "Concentrated Risk Taker",
    2: "Momentum-Driven Allocator",
    3: "Balanced Growth Seeker"
}

behavior_label = cluster_labels.get(cluster_id, "Unknown Profile")

summary_text, insight_list = generate_behavior_insight(
    hhi,
    portfolio_vol,
    corr_exposure,
    behavior_label
)

# -----------------------------
# Main Title
# -----------------------------

st.title("🧠 Behavioral Risk Radar")

st.markdown("""
This AI-powered feature evaluates your portfolio's structural risk profile 
by combining quantitative metrics, clustering models, and stress simulations.

**What it does:**
- Measures diversification and concentration
- Classifies behavioral risk profile
- Simulates forward stress scenarios
- Generates portfolio-level insights
""")

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

    col1.metric("Annualized Volatility", f"{portfolio_vol:.2%}")
    col2.metric("Concentration (HHI)", f"{hhi:.3f}")
    col3.metric("Behavior Profile", behavior_label)

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

    if selected_assets and total_weight == 100:

        normalized_vol = min(portfolio_vol / 0.4, 1)
        normalized_hhi = min(hhi, 1)
        normalized_corr = min(max(corr_exposure, 0), 1)

        radar_data = pd.DataFrame({
            "Metric": ["Volatility", "Concentration", "Correlation"],
            "Score": [normalized_vol, normalized_hhi, normalized_corr]
        })

        fig = px.line_polar(
            radar_data,
            r="Score",
            theta="Metric",
            line_close=True
        )

        fig.update_traces(fill='toself')
        fig.update_layout(title="Normalized Risk Profile")

        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 3 - Stress Test
# -----------------------------

with tab3:
    st.header("Monte Carlo Stress Simulation")

    if selected_assets and total_weight == 100:

        horizon = st.slider("Time Horizon (Days)", 30, 365, 180)
        confidence = st.slider("Confidence Level (%)", 90, 99, 95)

        with st.spinner("Running Monte Carlo simulation..."):

            simulations = run_monte_carlo_simulation(
                weights,
                returns,
                horizon_days=horizon
            )

            var, es = compute_var_es(
                simulations,
                confidence_level=confidence
            )

        col1, col2 = st.columns(2)

        col1.metric("Value at Risk (VaR)", f"{var:.2%}")
        col2.metric("Expected Shortfall (CVaR)", f"{es:.2%}")

        fig = px.histogram(simulations, nbins=50)
        fig.update_layout(title="Distribution of Simulated Portfolio Returns")
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 4 - AI Insights
# -----------------------------

with tab4:
    st.header("Behavioral AI Insights")

    if selected_assets and total_weight == 100:

        st.success(summary_text)

        st.markdown("### Key Risk Observations")

        for insight in insight_list:
            st.write(f"- {insight}")

        st.markdown("### Suggested Considerations")

        if hhi > 0.5:
            st.write("- Consider increasing diversification across sectors or asset classes.")

        if portfolio_vol > 0.25:
            st.write("- Introduce lower-volatility or defensive assets.")

        if corr_exposure > 0.6:
            st.write("- Reduce correlation by mixing equities with bonds or commodities.")

        if hhi < 0.3 and portfolio_vol < 0.18:
            st.write("- Your portfolio structure appears balanced. Monitor periodically.")