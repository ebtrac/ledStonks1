import yfinance as yf

stocks = 'MSFT'
data = yf.download(tickers = stocks, period='1d',interval='1m')

opens = data['Open']
graph_height = 31
# scale between 0 and graph_height
scl_opens = opens - min(opens)
scl_opens = round(scl_opens * graph_height / max(scl_opens))
print(scl_opens)
