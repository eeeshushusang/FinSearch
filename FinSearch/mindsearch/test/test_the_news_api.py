# test_the_news_api.py

import logging
from lagent.actions.the_news_api import ActionTheNewsAPI

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_search_news():
    # 初始化 ActionTheNewsAPI 实例
    api_key = 'VSgvqN78F2CQLncIDgubkFupfiIVUcnytpUGeQrx'  # 替换为您的 The News API 密钥
    news_api = ActionTheNewsAPI(api_key=api_key)

    # 定义测试查询
    query = "苹果公司 股票 投资建议"
    language = 'zh'
    page_size = 5

    # 调用 search_news 方法
    results = news_api.search_news(query=query, page_size=page_size, language=language)

    # 打印结果
    if results and 'data' in results:
        print(f"收到 {len(results['data'])} 条新闻:")
        for idx, article in enumerate(results['data'], start=1):
            title = article.get('title', '无标题')
            description = article.get('description', '无描述')
            url = article.get('url', '无链接')
            print(f"{idx}. {title}: {description} [{url}]")
    else:
        print("未能获取到新闻数据。")

if __name__ == "__main__":
    test_search_news()
