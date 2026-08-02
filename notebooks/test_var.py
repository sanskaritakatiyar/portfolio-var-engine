import sys
sys.path.append('../src')

import numpy as np
from database import load_returns
from var_engine import historical_var, parametric_var, monte_carlo_var, expected_shortfall, portfolio_var

# Load returns
tickers = ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'GS']
returns_df = load_returns(tickers, db_path='../data/portfolio.db')

# Equal weights portfolio
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

# Compute portfolio returns
portfolio_returns = returns_df.dot(weights)

# Compute VaR three ways
h_var = historical_var(portfolio_returns.values)
p_var = parametric_var(portfolio_returns.values)
mc_var = monte_carlo_var(portfolio_returns.values)
es = expected_shortfall(portfolio_returns.values)

print(f"Portfolio VaR (95% confidence, 1-day):")
print(f"  Historical  : {h_var:.4f} ({h_var*100:.2f}%)")
print(f"  Parametric  : {p_var:.4f} ({p_var*100:.2f}%)")
print(f"  Monte Carlo : {mc_var:.4f} ({mc_var*100:.2f}%)")
print(f"  Exp Shortfall: {es:.4f} ({es*100:.2f}%)")