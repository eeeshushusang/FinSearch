from lagent.actions.yahoo_finance import ActionYahooFinance

# 初始化操作类
yahoo_finance = ActionYahooFinance()

# 获取股票实时行情数据
quote = yahoo_finance.get_stock_quote(symbol='AAPL')
print(quote)

# 获取公司简介
profile = yahoo_finance.get_company_profile(symbol='AAPL')
print(profile)

# 获取股票历史价格数据
historical_prices = yahoo_finance.get_historical_prices(symbol='AAPL', period='1mo', interval='1d')
print(historical_prices)
