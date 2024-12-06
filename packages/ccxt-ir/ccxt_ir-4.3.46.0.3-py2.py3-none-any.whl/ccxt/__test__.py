from abantether import abantether
exchange = abantether()

# Fetch the ticker for BTCUSDT
ticker = exchange.fetch_ticker('BTC/USDT')

print(ticker)