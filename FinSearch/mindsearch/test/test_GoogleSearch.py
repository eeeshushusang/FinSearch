from lagent.actions import GoogleSearch

def test_google_search():
    API_KEY = '95db38c6b511d9ea6f00ef87a0cfba7b91a3c22b'
    # 初始化GoogleSearch
    search = GoogleSearch(api_key=API_KEY)

    # 定义搜索查询
    query = "Microsoft Corporation market analysis September 2024"
    
    try:
        # 执行搜索
        results = search.run(query,10)  # 假设`run`方法接受查询字符串
        
        # 打印搜索结果
        print(f"搜索查询: {query}")
        print("搜索结果:")
        print(results)
        # for idx, item in enumerate(results, start=1):
        #     print(f"{idx}. 标题: {item.get('title')}")
        #     print(f"   链接: {item.get('link')}")
        #     print(f"   摘要: {item.get('snippet')}\n")
    except Exception as e:
        print(f"搜索过程中出现错误: {e}")

if __name__ == "__main__":
    test_google_search()
