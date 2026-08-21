import numpy as np

def generate_random_portfolios(returns_df, n_portfolios=5000):
    """
    Generate n_portfolios random weight combinations and calculate
    their risk (volatility) and return.
    """
    n_assets = returns_df.shape[1]
    results = []
    
    mean_returns = returns_df.mean()
    cov_matrix = returns_df.cov()
    
    for _ in range(n_portfolios):
        weights = np.random.random(n_assets)
        weights = weights / weights.sum()
        
        portfolio_return = np.dot(weights, mean_returns) * 252  # annualized
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance) * np.sqrt(252)  # annualized
        
        results.append({
            'weights': weights,
            'return': portfolio_return,
            'volatility': portfolio_volatility
        })
    
    return results

def find_min_variance_portfolio(portfolios):
    """
    Find the portfolio with the lowest volatility among all generated.
    """
    min_vol_portfolio = min(portfolios, key=lambda p: p['volatility'])
    return min_vol_portfolio