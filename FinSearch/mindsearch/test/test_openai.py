from lagent.llms import GPTAPI

llm = GPTAPI(model_type='gpt-4o-mini', key='sk-4uZCkc6LuWsSHhUL0e651401E5974e07A1AfA4A4D483418a')

messages = [
    {"role": "system", "content": "你是一个有用的Agent"},
    {"role": "user", "content": "告诉我今天的天气怎么样"}
]

# 调用 chat 方法并获取响应
response = llm.chat(inputs=messages)

print(response)
# from openai import OpenAI
# client = OpenAI(
#     api_key='sk-4uZCkc6LuWsSHhUL0e651401E5974e07A1AfA4A4D483418a',
#     base_url="https://fast.bemore.lol/v1"
# )
# model_name = "gpt-4o-mini"
# response = client.chat.completions.create(
#     model=model_name,
#     messages=[
#         {"role": "system", "content": "你是一个擅长python编程的Agent,可以用中文回答问题，并编写代码.对于我的问题，你需要读取我给你的代码和指示，根据指示修改代码，并作出说明，仅回复你修改的部分代码，不要回复完整代码"},
#         {"role": "user", "content": """
# 为我推荐一部少女漫画
# """
# },
#     ],
#     temperature=0.8,
#     top_p=0.8
# )
# print(response.choices[0].message.content)
