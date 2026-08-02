import numpy as np
from scipy.stats import norm

def historical_var(returns, confidence=0.95):
    """
    VaR using actual historical returns.
    Sort past returns and find the worst (1-confidence)% day.
    """
    return np.percentile(returns, (1 - confidence) * 100)

def parametric_var(returns, confidence=0.95):
    """
    VaR assuming returns are normally distributed.
    Uses mean and std dev of historical returns.
    """
    mu = np.mean(returns)
    sigma = np.std(returns)
    return norm.ppf(1 - confidence, mu, sigma)

def monte_carlo_var(returns, confidence=0.95, n_simulations=10000):
    """
    VaR by simulating thousands of future return scenarios.
    Randomly samples from a normal distribution fitted to historical returns.
    """
    mu = np.mean(returns)
    sigma = np.std(returns)
    simulated = np.random.normal(mu, sigma, n_simulations)
    return np.percentile(simulated, (1 - confidence) * 100)

def expected_shortfall(returns, confidence=0.95):
    """
    CVaR / Expected Shortfall: average loss on the worst days beyond VaR.
    More informative than VaR alone — tells you how bad the bad days really are.
    """
    var = historical_var(returns, confidence)
    tail_losses = returns[returns <= var]
    return tail_losses.mean()

def portfolio_var(weights, returns_df, method='historical', confidence=0.95):
    """
    Compute VaR for a portfolio given asset weights and individual asset returns.
    weights: list of weights (must sum to 1), e.g. [0.4, 0.3, 0.3]
    returns_df: DataFrame where each column is one asset's daily returns
    """
    portfolio_returns = returns_df.dot(weights)
    
    if method == 'historical':
        return historical_var(portfolio_returns, confidence)
    elif method == 'parametric':
        return parametric_var(portfolio_returns, confidence)
    elif method == 'monte_carlo':
        return monte_carlo_var(portfolio_returns, confidence)