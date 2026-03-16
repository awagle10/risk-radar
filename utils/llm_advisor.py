import cohere
import os


def generate_ai_portfolio_analysis(
    volatility,
    hhi,
    correlation,
    var,
    expected_shortfall,
    cluster_label
):

    api_key = os.getenv("COHERE_API_KEY")

    if api_key is None:
        return "LLM analysis unavailable. Please configure COHERE_API_KEY."

    co = cohere.ClientV2(api_key)

    prompt = f"""
You are a professional portfolio risk analyst.

Analyze the following portfolio metrics and produce a concise risk report.

Portfolio Metrics:
Volatility: {volatility}
Concentration (HHI): {hhi}
Correlation Exposure: {correlation}
Value at Risk: {var}
Expected Shortfall: {expected_shortfall}
Behavioral Profile: {cluster_label}

Tasks:
1. Interpret the portfolio risk structure
2. Identify key vulnerabilities
3. Suggest improvements to reduce downside risk
4. Explain reasoning clearly
"""

    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.3)

    return response.message.content[0].text