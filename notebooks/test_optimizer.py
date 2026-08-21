import sys
sys.path.append('../src')

from database import load_returns
from optimizer import generate_random_portfolios, find_min_variance_portfolio

tickers = ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'GS']
returns_df = load_returns(tickers, db_path='../data/portfolio.db')

portfolios = generate_random_portfolios(returns_df, n_portfolios=5000)
best = find_min_variance_portfolio(portfolios)

print("Minimum Variance Portfolio:")
print(f"  Expected annual return: {best['return']*100:.2f}%")
print(f"  Annual volatility: {best['volatility']*100:.2f}%")
print(f"  Weights:")
for ticker, w in zip(tickers, best['weights']):
    print(f"    {ticker}: {w*100:.1f}%")