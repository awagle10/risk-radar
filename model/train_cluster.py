import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import joblib
import os


# -----------------------------
# Generate Synthetic Portfolios
# -----------------------------

def generate_synthetic_portfolios(n_samples=2000):
    """
    Generate synthetic investor risk profiles.
    Each profile has:
    - HHI (concentration)
    - Volatility
    - Correlation exposure
    """

    data = []

    for _ in range(n_samples):

        # Randomly simulate concentration
        hhi = np.random.uniform(0.15, 1.0)

        # Volatility correlated loosely with concentration
        volatility = np.random.normal(
            loc=0.15 + 0.2 * hhi,
            scale=0.05
        )

        volatility = max(0.05, volatility)

        # Correlation exposure loosely related to concentration
        correlation = np.random.uniform(0.1, 0.9) * hhi

        data.append([hhi, volatility, correlation])

    df = pd.DataFrame(
        data,
        columns=["HHI", "Volatility", "Correlation"]
    )

    return df


# -----------------------------
# Train Clustering Model
# -----------------------------

def train_cluster_model():

    df = generate_synthetic_portfolios()

    X = df[["HHI", "Volatility", "Correlation"]]

    model = KMeans(n_clusters=4, random_state=42)
    model.fit(X)

    os.makedirs("model", exist_ok=True)

    joblib.dump(model, "model/risk_cluster_model.pkl")

    print("Clustering model trained and saved successfully.")


if __name__ == "__main__":
    train_cluster_model()