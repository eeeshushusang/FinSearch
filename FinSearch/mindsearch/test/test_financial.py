from lagent.actions.financial import ActionFMPAPI

# 初始化操作类，替换为您的 API 密钥
fmp_api = ActionFMPAPI(api_key='fMIys2CnEMTos9tMJzzulUitr8Q3Ffrv')

# 获取股票实时报价
quote = fmp_api.get_stock_quote(symbol='AAPL')
print(quote)

# 获取公司简介
profile = fmp_api.get_company_profile(symbol='AAPL')
print(profile)

# 获取股票历史价格数据
historical_prices = fmp_api.get_historical_prices(symbol='AAPL', timeframe='1month')
print(historical_prices)
