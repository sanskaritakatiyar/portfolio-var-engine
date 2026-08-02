import sqlite3
import pandas as pd
import yfinance as yf

def build_database(tickers, db_path='data/portfolio.db'):
    """
    Download price data for given tickers and store in SQLite database.
    Creates two tables: prices and returns.
    """
    conn = sqlite3.connect(db_path)
    
    for ticker in tickers:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker, period='5y', auto_adjust=True)['Close']
        df = df.reset_index()
        df.columns = ['date', 'close']
        df['ticker'] = ticker
        df.to_sql('prices', conn, if_exists='append', index=False)
    
    print("Building returns table...")
    conn.execute("DROP TABLE IF EXISTS returns")
    conn.execute("""
        CREATE TABLE returns AS
        SELECT 
            ticker,
            date,
            (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
            / LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS daily_return
        FROM prices
    """)
    
    conn.commit()
    conn.close()
    print("Database built successfully.")

def load_returns(tickers, db_path='data/portfolio.db'):
    """
    Load returns from database into a DataFrame.
    Each column = one ticker's daily returns.
    """
    conn = sqlite3.connect(db_path)
    
    dfs = []
    for ticker in tickers:
        query = f"""
            SELECT date, daily_return 
            FROM returns 
            WHERE ticker = '{ticker}' 
            AND daily_return IS NOT NULL
            ORDER BY date
        """
        df = pd.read_sql(query, conn, index_col='date')
        df.columns = [ticker]
        dfs.append(df)
    
    conn.close()
    returns_df = pd.concat(dfs, axis=1).dropna()
    return returns_df

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'GS']
    build_database(tickers)
    returns = load_returns(tickers)
    print(returns.tail())
    print(f"\nLoaded {len(returns)} days of returns for {len(tickers)} assets")