# test_news_search_agent.py

import logging
from mindsearch.agent.mindsearch_agent import NewsSearchAgent
from lagent.llms import GPTAPI
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_news_search_agent():
    api_key = 'VSgvqN78F2CQLncIDgubkFupfiIVUcnytpUGeQrx' 
    template = {
        "input": "根据以下新闻文章回答问题：\n{context}\n问题：{query}",
        "context": "历史问题：{question}\n回答：{answer}\n"
    }
    news_agent = NewsSearchAgent(api_key=api_key, template=template,llm = GPTAPI(model_type='gpt-4o-mini', key='sk-4uZCkc6LuWsSHhUL0e651401E5974e07A1AfA4A4D483418a')
)

    # 定义测试查询和父响应
    question = "苹果公司的最新产品发布有哪些？"
    parent_response = [
        {'question': '苹果公司的最近的新闻是什么？', 'answer': '苹果公司最近发布了新款iPhone和Apple Watch系列。'}
    ]

    # 调用 stream_chat 方法并打印输出
    print("测试 NewsSearchAgent:")
    for agent_return in news_agent.stream_chat(question, parent_response=parent_response):
        print(agent_return.response)

if __name__ == "__main__":
    test_news_search_agent()
