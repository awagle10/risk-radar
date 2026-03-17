from groq import Groq
import os
import json
import re
import streamlit as st


@st.cache_data(ttl=300)
def get_ai_response(prompt, api_key):
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # free + fast
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content


def generate_ai_portfolio_analysis(
    volatility,
    hhi,
    correlation,
    var,
    expected_shortfall,
    cluster_label
):

    api_key = os.getenv("GROQ_API_KEY")

    if api_key is None:
        return "LLM analysis unavailable. Please configure GROQ_API_KEY.", None

    prompt = f"""
    You are a professional portfolio risk analyst.

    Analyze the portfolio metrics below and produce a structured report.

    Portfolio Metrics:
    Volatility: {volatility}
    Concentration (HHI): {hhi}
    Correlation Exposure: {correlation}
    Value at Risk: {var}
    Expected Shortfall: {expected_shortfall}
    Behavioral Profile: {cluster_label}

    First provide a concise risk report.

    Then output a JSON block with risk scores from 1-10 for the following:

    - diversification_risk
    - volatility_risk
    - correlation_risk
    - tail_risk

    Example JSON format:

    {{
    "diversification_risk": 7,
    "volatility_risk": 6,
    "correlation_risk": 8,
    "tail_risk": 7
    }}
    """

    
    text_output = get_ai_response(prompt, api_key)

    json_match = re.search(r"\{.*\}", text_output, re.DOTALL)

    risk_scores = None

    if json_match:
        try:
            risk_scores = json.loads(json_match.group())
        except:
            risk_scores = None
                                                    
    return text_output, risk_scores


    

