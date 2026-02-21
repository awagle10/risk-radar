def generate_behavior_insight(hhi, volatility, correlation, cluster_label):
    """
    Generate behavioral interpretation based on risk metrics.
    """

    insights = []

    # Concentration logic
    if hhi > 0.5:
        insights.append("Your portfolio is highly concentrated, which increases idiosyncratic risk.")
    elif hhi > 0.3:
        insights.append("Your portfolio shows moderate concentration.")
    else:
        insights.append("Your portfolio appears well diversified.")

    # Volatility logic
    if volatility > 0.25:
        insights.append("You are exposed to high volatility assets.")
    elif volatility > 0.18:
        insights.append("Your volatility exposure is moderate.")
    else:
        insights.append("Your portfolio volatility is relatively controlled.")

    # Correlation logic
    if correlation > 0.6:
        insights.append("Assets in your portfolio are highly correlated, increasing systemic risk.")
    elif correlation > 0.3:
        insights.append("There is moderate correlation between your holdings.")
    else:
        insights.append("Your assets show relatively low correlation.")

    # Behavioral summary
    summary = f"You are classified as a '{cluster_label}'. This reflects your portfolio's structural risk profile."

    return summary, insights