import yfinance as yf 
from lagent.actions.base_action import BaseAction, tool_api
from .parser import BaseParser, JsonParser
from typing import List, Optional, Tuple, Type, Union
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

class ActionYahooFinance(BaseAction):
    """
    使用 Yahoo Finance API 获取金融数据的操作类。
    """
    def __init__(self,
                description: Optional[dict] = None,
                parser: Type[BaseParser] = JsonParser,
                enable: bool = True):
        super().__init__(description, parser, enable)
        self._name = "Finance"
    
    @tool_api
    def get_stock_quote(self, symbol):
        """
        获取指定股票的实时行情数据。

        :param symbol: 股票代码，例如 'AAPL'、'GOOG'
        :return: 包含股票行情数据的字典
        """
        stock = yf.Ticker(symbol)
        data = stock.info
        return data

    @tool_api
    def get_historical_prices(self, symbol, period='1mo', interval='1d'):
        """
        获取指定股票的历史价格数据，并生成并显示 K 线图。

        :param symbol: 股票代码
        :param period: 数据时间范围，例如 '1d'、'5d'、'1mo'、'3mo'、'6mo'、'1y'、'2y'、'5y'、'10y'、'max'
        :param interval: 数据间隔，例如 '1m'、'2m'、'5m'、'15m'、'30m'、'60m'、'90m'、'1h'、'1d'、'5d'、'1wk'、'1mo'、'3mo'
        :return: 包含历史价格的 DataFrame
        """
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            raise ValueError("没有获取到历史价格数据。")
        # try:
        #     fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
            
        #     # 添加 K 线图
        #     fig.add_trace(go.Candlestick(
        #         x=hist.index,
        #         open=hist['Open'],
        #         high=hist['High'],
        #         low=hist['Low'],
        #         close=hist['Close'],
        #         name='K线',
        #         increasing_line_color='green',
        #         decreasing_line_color='red',
        #         showlegend=True
        #     ))

        #     # 添加收盘价连接线
        #     fig.add_trace(go.Scatter(
        #         x=hist.index,
        #         y=hist['Close'],
        #         mode='lines',
        #         line=dict(color='yellow', width=1),
        #         name='收盘价',
        #         showlegend=True
        #     ))

        #     # 计算趋势线（线性回归）
        #     # 将日期转换为数值
        #     x_numeric = hist.index.map(datetime.toordinal)
        #     y = hist['Close']
        #     # 进行线性回归
        #     slope, intercept = np.polyfit(x_numeric, y, 1)
        #     trend = slope * x_numeric + intercept

        #     # 添加趋势线
        #     fig.add_trace(go.Scatter(
        #         x=hist.index,
        #         y=trend,
        #         mode='lines',
        #         line=dict(color='orange', width=2, dash='dash'),
        #         name='趋势线',
        #         showlegend=True
        #     ))

        #     # 更新布局
        #     fig.update_layout(
        #         title=f"{symbol} K线图",
        #         yaxis_title='价格 (USD)',
        #         xaxis_title='日期',
        #         xaxis_rangeslider_visible=False,  # 隐藏范围滑块
        #         template='plotly_dark',  
        #         legend=dict(
        #             orientation="h",
        #             yanchor="bottom",
        #             y=1.02,
        #             xanchor="right",
        #             x=1
        #         ),
        #         hovermode='x unified'
        #     )

        #     # 更新 x 轴的范围显示
        #     fig.update_xaxes(
        #         rangeslider_visible=False,
        #         rangeselector=dict(
        #             buttons=list([
        #                 dict(count=1, label="1m", step="month", stepmode="backward"),
        #                 dict(count=3, label="3m", step="month", stepmode="backward"),
        #                 dict(count=6, label="6m", step="month", stepmode="backward"),
        #                 dict(step="all")
        #             ])
        #         )
        #     )

        #     # 设置图表尺寸
        #     fig.update_layout(
        #         width=1000,
        #         height=600
        #     )

        #     # 立即显示图表
        #     fig.show()
        # except Exception as e:
        #     logger.exception(f"绘制 K 线图时发生错误: {e}")
        #     raise e
        return hist

    def execute(self, question: str):
        """
        兼容 ActionExecutor 的 execute 方法，只接受问题，不使用父响应。
        根据问题内容调用相应的方法获取金融数据并返回 AgentReturn 对象。
        """
        try:
            logger.debug(f"ActionYahooFinance 开始处理问题: {question}")

            # 简单解析问题，提取股票代码
            import re
            match = re.search(r'([A-Z]{1,5})', question)
            if match:
                symbol = match.group(1)
            else:
                symbol = 'AAPL'  # 默认股票代码，可根据需要调整

            # 获取股票报价
            quote = self.get_stock_quote(symbol)
            logger.debug(f"获取的股票报价: {quote}")

            # 获取公司简介
            profile = self.get_company_profile(symbol)
            logger.debug(f"获取的公司简介: {profile}")

            response_text = f"股票代码 **{symbol}** 的最新行情数据如下：\n" \
                            f"名称：{profile.get('longName', 'N/A')}\n" \
                            f"当前价格：{quote.get('currentPrice', 'N/A')} USD\n" \
                            f"市场资本：{quote.get('marketCap', 'N/A')}\n" \
                            f"PE 比率：{quote.get('trailingPE', 'N/A')}\n" \
                            f"公司简介：{profile.get('longBusinessSummary', 'N/A')}\n"

            logger.debug(f"生成的响应文本: {response_text}")

            # 创建 AgentReturn 对象
            agent_return = AgentReturn(response=response_text, detail={"source": "ActionYahooFinance"})
            agent_return.type = "finance_search"
            agent_return.content = question

            logger.debug(f"生成的 AgentReturn 对象: {agent_return.response}")
            yield deepcopy(agent_return)

        except Exception as e:
            logger.exception(f"ActionYahooFinance 执行过程中发生错误: {e}")
            agent_return = AgentReturn(response="获取金融数据时发生错误。", detail={"error": str(e)})
            agent_return.type = "finance_search"
            agent_return.content = question
            yield deepcopy(agent_return)
            
