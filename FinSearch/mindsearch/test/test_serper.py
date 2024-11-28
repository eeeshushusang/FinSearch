import os
import requests

def test_serper_api():
    API_KEY = os.getenv('SERPER_API_KEY', '95db38c6b511d9ea6f00ef87a0cfba7b91a3c22b')  # 替换为您的 API 密钥
    query = "上海今天的天气"
    
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json',
    }
    data = {
        'q': query
    }
    
    try:
        response = requests.post(
            'https://google.serper.dev/search',
            headers=headers,
            json=data,
            timeout=5
        )
        if response.status_code == 200:
            print("API 调用成功，响应内容:")
            print(response.json())
        else:
            print(f"API 调用失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求过程中出现异常: {e}")

if __name__ == "__main__":
    test_serper_api()
