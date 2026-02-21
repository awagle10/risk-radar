import numpy as np


def run_monte_carlo_simulation(weights_dict, returns, horizon_days=180, n_simulations=1000):
    """
    Monte Carlo simulation using multivariate normal distribution.
    """

    selected_assets = list(weights_dict.keys())
    weights = np.array(list(weights_dict.values())) / 100

    mean_returns = returns[selected_assets].mean()
    cov_matrix = returns[selected_assets].cov()

    simulations = []

    for _ in range(n_simulations):

        daily_returns = np.random.multivariate_normal(
            mean_returns,
            cov_matrix,
            horizon_days
        )

        portfolio_daily = np.dot(daily_returns, weights)

        cumulative_return = np.prod(1 + portfolio_daily) - 1

        simulations.append(cumulative_return)

    simulations = np.array(simulations)

    return simulations


def compute_var_es(simulations, confidence_level=95):
    """
    Compute Value at Risk and Expected Shortfall.
    """

    var_threshold = np.percentile(simulations, 100 - confidence_level)
    expected_shortfall = simulations[simulations <= var_threshold].mean()

    return var_threshold, expected_shortfall