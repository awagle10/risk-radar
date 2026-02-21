import pandas as pd
import numpy as np


import os

def load_price_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "historical_prices.csv")

    df = pd.read_csv(file_path, parse_dates=["Date"])
    prices = df.pivot(index="Date", columns="Ticker", values="Adj Close")
    return prices


def compute_daily_returns(prices):
    """
    Compute daily percentage returns.
    """
    returns = prices.pct_change().dropna()
    return returns


def compute_portfolio_volatility(weights_dict, returns):
    """
    Compute annualized portfolio volatility.
    """
    weights = np.array(list(weights_dict.values())) / 100
    selected_assets = list(weights_dict.keys())

    cov_matrix = returns[selected_assets].cov()
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))

    annualized_volatility = np.sqrt(portfolio_variance) * np.sqrt(252)

    return annualized_volatility


def compute_hhi(weights_dict):
    """
    Compute Herfindahl-Hirschman Index (concentration).
    """
    weights = np.array(list(weights_dict.values())) / 100
    hhi = np.sum(weights ** 2)
    return hhi


def compute_correlation_exposure(weights_dict, returns):
    """
    Compute weighted average pairwise correlation.
    """
    selected_assets = list(weights_dict.keys())
    corr_matrix = returns[selected_assets].corr()

    weights = np.array(list(weights_dict.values())) / 100

    weighted_corr = 0
    total_weight = 0

    for i in range(len(weights)):
        for j in range(i + 1, len(weights)):
            pair_weight = weights[i] * weights[j]
            weighted_corr += pair_weight * corr_matrix.iloc[i, j]
            total_weight += pair_weight

    if total_weight == 0:
        return 0

    return weighted_corr / total_weight