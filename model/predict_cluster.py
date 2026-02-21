import joblib
import numpy as np


import os

def load_cluster_model():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(base_dir, "model", "risk_cluster_model.pkl")

    return joblib.load(model_path)


def predict_behavior_cluster(hhi, volatility, correlation):
    model = load_cluster_model()

    X = np.array([[hhi, volatility, correlation]])

    cluster = model.predict(X)[0]

    return cluster