# Portfolio VaR Engine

A deployable portfolio risk management tool built in Python, with a live interactive dashboard covering Value at Risk, stress testing, and portfolio optimization.

**Live demo: https://portfolio-var-engine-azpx8ngxgp2t3wutveufkj.streamlit.app/**

*(Note: free-tier hosting sleeps after inactivity — click "wake up app" if it shows a sleep screen, takes ~30-60 seconds to restart)*

## What it does
- Computes Value at Risk (VaR) using 3 methods: Historical Simulation, Parametric, and Monte Carlo
- Calculates Expected Shortfall (CVaR) — the average loss beyond the VaR threshold
- Runs stress tests against 4 historical crisis scenarios: GFC 2008, COVID crash, Russia-Ukraine 2022, Tech Selloff 2022 — with both tabular and visual (bar chart) output
- Custom portfolio weights via interactive sliders, normalized so they always sum to 100%
- Shows asset correlation heatmap to visualize diversification benefit between holdings
- Portfolio optimization: generates 1,000+ random weight combinations and plots the risk-return efficient frontier, identifying the minimum variance portfolio
- Built on 18 years of real market data (2007–present) stored in a SQLite database

## Sample results (equal-weighted AAPL, MSFT, GOOGL, JPM, GS, 95% confidence)
Historical VaR   : -2.35%
Parametric VaR   : -2.55%
Monte Carlo VaR  : -2.55%
Expected Shortfall: -3.72%

GFC 2008 (Sep-Nov)        : -33.72% total loss, -13.16% worst day
COVID Crash (Feb-Mar 2020): -21.12% total loss, -13.38% worst day

Minimum variance portfolio (from 5,000 simulations):
  Expected annual return: 22.06% | Annual volatility: 24.44%
  Weights: AAPL 20.9% | MSFT 38.5% | GOOGL 23.1% | JPM 10.1% | GS 7.3%

## Tech stack
Python · NumPy · Pandas · SciPy · Plotly · Streamlit · SQLite · SQLAlchemy · yfinance

## Project structure
portfolio-var-engine/
├── src/
│ ├── var_engine.py # 3 VaR methods + Expected Shortfall
│ ├── database.py # SQLite database build and query layer
│ ├── stress_test.py # Historical crisis scenario analysis
│ └── optimizer.py # Monte Carlo portfolio optimization
├── notebooks/
│ ├── test_var.py
│ ├── test_optimizer.py
│ └── frontier_plot.py
├── app.py # Streamlit dashboard
├── data/ # SQLite database
└── README.md

## How to run locally
pip install -r requirements.txt
python src/database.py     # builds the database
streamlit run app.py       # launches the dashboard

## Key concepts demonstrated
- Value at Risk methodology (historical, parametric, Monte Carlo) — FRM Readings 47-48
- Expected Shortfall as a coherent risk measure superior to VaR — FRM Reading 47
- Stress testing methodology and its role alongside statistical risk measures — FRM Reading 54
- Modern Portfolio Theory and the efficient frontier — diversification benefit quantified via covariance
- SQL window functions for time-series financial calculations

## Next steps
- Add historical GFC/COVID data coverage for additional asset classes
- Backtest VaR predictions against realized returns (Kupiec test)

