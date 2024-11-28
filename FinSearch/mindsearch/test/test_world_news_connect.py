import requests
from config import API_KEYS
QUERY = 'Microsoft'  # 替换为你想查询的关键词

def get_world_news(api_key, query, language='zh', page=1, page_size=5):
    url = 'https://world-news-api.com/api/v1/news'
    params = {
        'apiKey': api_key,
        'query': query,
        'language': language,
        'page': page,
        'pageSize': page_size
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

if __name__ == "__main__":
    news_data = get_world_news(API_KEYS['worldnewsapi'], QUERY)
    if news_data:
        print(news_data)  # 输出返回的新闻数据
