import yfinance as yf
#yf.download('AAPL').to_csv('data/AAPL.csv')
data = yf.download('MSFT')
data.to_csv('data/MSFT.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])
