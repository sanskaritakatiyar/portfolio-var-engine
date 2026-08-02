import numpy as np
import pandas as pd

SCENARIOS = {
    'GFC 2008 (Sep-Nov)': ('2008-09-01', '2008-11-30'),
    'COVID Crash (Feb-Mar 2020)': ('2020-02-01', '2020-03-31'),
    'Russia-Ukraine 2022': ('2022-02-01', '2022-03-31'),
    'Tech Selloff 2022': ('2022-01-01', '2022-06-30'),
}

def run_stress_tests(weights, returns_df):
    """
    Apply historical crisis scenarios to current portfolio weights.
    Returns a dict of scenario name -> total portfolio loss during that period.
    """
    results = {}
    weights = np.array(weights)
    
    for scenario_name, (start, end) in SCENARIOS.items():
        try:
            scenario_returns = returns_df.loc[start:end]
            
            if len(scenario_returns) == 0:
                results[scenario_name] = None
                continue
            
            portfolio_daily = scenario_returns.dot(weights)
            total_loss = (1 + portfolio_daily).prod() - 1
            worst_day = portfolio_daily.min()
            
            results[scenario_name] = {
                'total_loss': round(total_loss * 100, 2),
                'worst_day': round(worst_day * 100, 2),
                'days': len(scenario_returns)
            }
        except Exception:
            results[scenario_name] = None
    
    return results

if __name__ == "__main__":
    import sys
    sys.path.append('src')
    from database import load_returns
    
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'GS']
    returns_df = load_returns(tickers, db_path='data/portfolio.db')
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]
    
    results = run_stress_tests(weights, returns_df)
    
    print("Stress Test Results:")
    print("-" * 50)
    for scenario, result in results.items():
        if result:
            print(f"\n{scenario}")
            print(f"  Total loss : {result['total_loss']}%")
            print(f"  Worst day  : {result['worst_day']}%")
            print(f"  Trading days: {result['days']}")
        else:
            print(f"\n{scenario}: No data available")