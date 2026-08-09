import sys
sys.path.append('src')

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from database import load_returns
from var_engine import historical_var, parametric_var, monte_carlo_var, expected_shortfall
from stress_test import run_stress_tests

st.set_page_config(page_title="Portfolio VaR Engine", layout="wide")
st.title("Portfolio VaR Engine")
st.caption("Value at Risk calculator with stress testing — built on 18 years of market data")

# Sidebar inputs
st.sidebar.header("Portfolio Settings")

available_tickers = ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'GS']
selected = st.sidebar.multiselect("Select assets", available_tickers, 
                                   default=available_tickers)

confidence = st.sidebar.slider("Confidence level", 0.90, 0.99, 0.95, step=0.01)

if len(selected) < 2:
    st.warning("Please select at least 2 assets.")
    st.stop()

st.sidebar.write("Set portfolio weights:")
raw_weights = []
for ticker in selected:
    w = st.sidebar.slider(f"{ticker} weight", 0, 100, 100 // len(selected), key=ticker)
    raw_weights.append(w)

raw_weights = np.array(raw_weights)

if raw_weights.sum() == 0:
    st.sidebar.warning("At least one weight must be greater than 0.")
    st.stop()

weights = raw_weights / raw_weights.sum()

st.sidebar.write("Normalized weights:")
for t, w in zip(selected, weights):
    st.sidebar.write(f"  {t}: {w:.1%}")
    
# Load data
returns_df = load_returns(selected, db_path='data/portfolio.db')
portfolio_returns = returns_df.dot(weights)

# VaR metrics
st.header("Value at Risk")
col1, col2, col3, col4 = st.columns(4)

h_var = historical_var(portfolio_returns.values, confidence)
p_var = parametric_var(portfolio_returns.values, confidence)
mc_var = monte_carlo_var(portfolio_returns.values, confidence)
es = expected_shortfall(portfolio_returns.values, confidence)

col1.metric("Historical VaR", f"{h_var*100:.2f}%")
col2.metric("Parametric VaR", f"{p_var*100:.2f}%")
col3.metric("Monte Carlo VaR", f"{mc_var*100:.2f}%")
col4.metric("Expected Shortfall", f"{es*100:.2f}%")

# Return distribution plot
st.header("Return Distribution")
fig = go.Figure()
fig.add_trace(go.Histogram(x=portfolio_returns.values, nbinsx=100, 
                            name='Daily Returns',
                            marker_color='steelblue', opacity=0.7))
fig.add_vline(x=h_var, line_dash="dash", line_color="red",
              annotation_text=f"VaR ({confidence:.0%})")
fig.update_layout(xaxis_title="Daily Return", yaxis_title="Frequency",
                  height=400)
st.plotly_chart(fig, use_container_width=True)

# Stress tests
st.header("Stress Test Scenarios")
stress_results = run_stress_tests(weights, returns_df)

stress_data = []
for scenario, result in stress_results.items():
    if result:
        stress_data.append({
            'Scenario': scenario,
            'Total Loss': f"{result['total_loss']}%",
            'Worst Day': f"{result['worst_day']}%",
            'Trading Days': result['days']
        })

if stress_data:
    st.dataframe(pd.DataFrame(stress_data), use_container_width=True)

# Correlation heatmap
st.header("Asset Correlation Matrix")
corr = returns_df.corr()
fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                      zmin=-1, zmax=1)
fig_corr.update_layout(height=400)
st.plotly_chart(fig_corr, use_container_width=True)

# Cumulative returns
st.header("Cumulative Portfolio Returns")
cum_returns = (1 + portfolio_returns).cumprod()
fig_cum = go.Figure()
fig_cum.add_trace(go.Scatter(x=cum_returns.index, y=cum_returns.values,
                              mode='lines', name='Portfolio',
                              line=dict(color='steelblue')))
fig_cum.update_layout(xaxis_title="Date", yaxis_title="Growth of $1",
                       height=400)
st.plotly_chart(fig_cum, use_container_width=True)