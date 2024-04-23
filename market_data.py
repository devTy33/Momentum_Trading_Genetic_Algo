import yfinance as yf
yf.download('AAPL').to_csv('data/MSFT.csv')