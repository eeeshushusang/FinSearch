import requests
import logging
from lagent.actions.base_action import BaseAction,tool_api
from .parser import BaseParser, JsonParser
from typing import Optional, Type
import os
import urllib

# 定义 logger
logger = logging.getLogger(__name__)

class ActionGNewsAPI(BaseAction):
    """
    使用 GNews API 获取新闻的操作类。
    """
    def __init__(self,
                api_key: str,
                description: Optional[dict] = None,
                parser: Type[BaseParser] = JsonParser,
                enable: bool = True):
        super().__init__(description, parser, enable)
        self.api_key = api_key
        self._name = "GNews"
    
    @tool_api
    def search_news(self, query: str, language='en', country='us', max_results=10):
        url = f"https://gnews.io/api/v4/search?q={urllib.parse.quote(query)}&lang={language}&country={country}&max={max_results}&apikey={self.api_key}"
        try:
            with requests.get(url) as response:
                response.raise_for_status()
                data = response.json()
                articles = data.get("articles", [])
                return articles
        except requests.exceptions.RequestException as e:
            logger.error(f"GNews API 请求失败: {e}")
            return []
