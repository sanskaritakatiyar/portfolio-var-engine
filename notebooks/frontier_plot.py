import sys
sys.path.append('../src')

import plotly.graph_objects as go
from database import load_returns
from optimizer import generate_random_portfolios, find_min_variance_portfolio

tickers = ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'GS']
returns_df = load_returns(tickers, db_path='../data/portfolio.db')

portfolios = generate_random_portfolios(returns_df, n_portfolios=5000)
best = find_min_variance_portfolio(portfolios)

returns = [p['return'] for p in portfolios]
vols = [p['volatility'] for p in portfolios]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=vols, y=returns, mode='markers',
    marker=dict(size=4, color=returns, colorscale='Viridis', showscale=True,
                colorbar=dict(title="Return")),
    name='Random portfolios'
))
fig.add_trace(go.Scatter(
    x=[best['volatility']], y=[best['return']],
    mode='markers', marker=dict(size=15, color='red', symbol='star'),
    name='Min variance portfolio'
))
fig.update_layout(
    title='Efficient Frontier — Risk vs Return',
    xaxis_title='Annual Volatility (Risk)',
    yaxis_title='Annual Expected Return',
    height=500
)
fig.write_html('../outputs/efficient_frontier.html')
print("Saved to outputs/efficient_frontier.html")