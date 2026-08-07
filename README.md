# Portfolio VaR Engine

A deployable portfolio risk management tool built in Python, with a live interactive dashboard.

**Live demo: https://portfolio-var-engine-azpx8ngxgp2t3wutveufkj.streamlit.app/**

## What it does
- Computes Value at Risk (VaR) using 3 methods: Historical Simulation, Parametric, and Monte Carlo
- Calculates Expected Shortfall (CVaR) — the average loss beyond the VaR threshold
- Runs stress tests against 4 historical crisis scenarios: GFC 2008, COVID crash, Russia-Ukraine 2022, Tech Selloff 2022
- Shows asset correlation heatmap and cumulative portfolio returns
- Built on 18 years of real market data stored in a SQLite database

## Sample results (equal-weighted AAPL, MSFT, GOOGL, JPM, GS)
Historical VaR  : -2.35%
Parametric VaR  : -2.55%
Monte Carlo VaR : -2.55%
Exp. Shortfall  : -3.72%

GFC 2008 (Sep-Nov)       : -33.72% total loss, -13.16% worst day
COVID Crash (Feb-Mar 2020): -21.12% total loss, -13.38% worst day

## Tech stack
Python · NumPy · Pandas · SciPy · Plotly · Streamlit · SQLite · SQLAlchemy · yfinance

## Project structure
portfolio-var-engine/
├── src/
│ ├── var_engine.py # 3 VaR methods + Expected Shortfall
│ ├── database.py # SQLite database build and query layer
│ └── stress_test.py # Historical crisis scenario analysis
├── app.py # Streamlit dashboard
├── data/ # SQLite database
└── README.md

## How to run locally
pip install -r requirements.txt
python src/database.py     # builds the database
streamlit run app.py       # launches the dashboard

## Next steps
- Custom portfolio weights (user input)
- Portfolio optimization (minimum variance frontier)
- Additional Indian market assets