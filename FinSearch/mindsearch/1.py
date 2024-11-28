from config import API_KEYS
from openai import OpenAI

client = OpenAI(
        api_key=API_KEYS['gpt'],
        base_url="https://fast.bemore.lol/v1/",
)

current_graph_info = 1  # 假设这是你要插入的变量值
chat_completion = client.chat.completions.create(
        messages=[
        {
                "role": "user",
                "content": f"{current_graph_info} 以下为final_response的其余prompt\n"
                           "然后基于提供的所有内容，撰写一篇详细完备的最终回答。\n"
                           "- 你需要显示地包含前面查询到的数值信息，这些数字必须是前面API获得的数据\n"
                           "- 回答内容需要逻辑清晰，层次分明，确保读者易于理解。\n"
                           "- 回答需要综合所有节点返回的数据与信息\n"
                           "- 回答中每个关键点需标注引用的搜索结果来源(保持跟问答对中的索引一致)，以确保信息的可信度。给出索引的形式为`[[int]]`，如果有多个索引，则用多个[[]]表示，如`[[id_1]][[id_2]]`。\n"
                           "- 回答部分需要全面且完备，不要出现'基于上述内容'等模糊表达，最终呈现的回答不包括提供给你的问答对。\n"
                           "- 语言风格需要专业、严谨，避免口语化表达。\n"
                           "- 保持统一的语法和词汇使用，确保整体文档的一致性和连贯性。\n"
                           "- 按时间和重要性顺序组织回答"
        }
    ],
    model="gpt-4o-mini",
)
print(chat_completion.choices[0].message.content)