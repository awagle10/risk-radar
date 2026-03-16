import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import joblib
import os

from utils.risk_metrics import (
    load_price_data,
    compute_daily_returns,
    compute_portfolio_volatility,
    compute_hhi,
    compute_correlation_exposure
)

# -----------------------------
# Generate Realistic Portfolios
# -----------------------------

def generate_portfolios(n_samples=3000):

    prices = load_price_data()
    returns = compute_daily_returns(prices)

    assets = returns.columns.tolist()

    portfolio_data = []

    for _ in range(n_samples):

        # Random portfolio weights
        weights_raw = np.random.random(len(assets))
        weights = weights_raw / weights_raw.sum()

        weights_dict = {
            asset: weight * 100
            for asset, weight in zip(assets, weights)
        }

        # Compute risk metrics
        volatility = compute_portfolio_volatility(weights_dict, returns)
        hhi = compute_hhi(weights_dict)
        correlation = compute_correlation_exposure(weights_dict, returns)

        portfolio_data.append([hhi, volatility, correlation])

    df = pd.DataFrame(
        portfolio_data,
        columns=["HHI", "Volatility", "Correlation"]
    )

    return df


# -----------------------------
# Train Clustering Model
# -----------------------------

def train_cluster_model():

    df = generate_portfolios()

    X = df[["HHI", "Volatility", "Correlation"]]

    model = KMeans(n_clusters=4, random_state=42)
    model.fit(X)

    os.makedirs("model", exist_ok=True)

    joblib.dump(model, "model/risk_cluster_model.pkl")

    print("Clustering model trained successfully.")


if __name__ == "__main__":
    train_cluster_model()