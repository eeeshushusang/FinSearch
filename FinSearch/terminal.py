from datetime import datetime

from lagent.actions import ActionExecutor, GoogleSearch
from lagent.llms import GPTAPI
from mindsearch.agent.mindsearch_agent import MindSearchAgent, MindSearchProtocol,SearcherAgent
from mindsearch.agent.mindsearch_prompt import (
    FINAL_RESPONSE_CN,
    FINAL_RESPONSE_EN,
    GRAPH_PROMPT_CN,
    GRAPH_PROMPT_EN,
    searcher_context_template_cn,
    searcher_context_template_en,
    searcher_input_template_cn,
    searcher_input_template_en,
    searcher_system_prompt_cn,
    searcher_system_prompt_en,
    finance_system_prompt_cn,
    finance_system_prompt_en,
    News_system_prompt_cn,
    News_system_prompt_en,
)
from lagent.actions.GNews_API import ActionGNewsAPI
from lagent.actions.yahoo_finance import ActionYahooFinance
from config import API_KEYS
import re
from tqdm import trange
import time
lang = "cn"
# llm = DeepseekAPI(model_type='deepseek-chat', key=API_KEYS['deepseek'])
# llm = GPTAPI(model_type="llama3.1-70b", key=API_KEYS['llama_api'],openai_api_base="https://api.llama-api.com/chat/completions")
# llm = GPTAPI(model_type="gpt-4o-mini", key=API_KEYS["gpt"],openai_api_base="https://api.openai.com/v1/chat/completions")
# llm = GPTAPI(model_type="claude-3-5-sonnet-20240620", key=API_KEYS['claude'],openai_api_base="https://api.xty.app/v1/chat/completions")
# llm = GPTAPI(model_type="claude-3-haiku", key=API_KEYS['claude'],openai_api_base="https://api.xty.app/v1/chat/completions")
llm = GPTAPI(model_type="gemini-1.5-flash-latest", key=API_KEYS['claude'],openai_api_base="https://api.xty.app/v1/chat/completions")
# llm = GPTAPI(model_type="deepseek-chat",key=API_KEYS['deepseek'],openai_api_base="https://api.deepseek.com/v1/chat/completions")


agent = MindSearchAgent(
    llm=llm,
    protocol=MindSearchProtocol(
        meta_prompt=datetime.now().strftime("The current date is %Y-%m-%d."),
        interpreter_prompt=GRAPH_PROMPT_CN if lang == "cn" else GRAPH_PROMPT_EN,
        response_prompt=FINAL_RESPONSE_CN if lang == "cn" else FINAL_RESPONSE_EN,
    ),
    searcher_cfg=dict(
        llm=llm,
        plugin_executor=ActionExecutor(
            GoogleSearch(api_key=API_KEYS["google_search"]),
        ),
        protocol=MindSearchProtocol(
            meta_prompt=datetime.now().strftime("The current date is %Y-%m-%d."),
            plugin_prompt=(
                searcher_system_prompt_cn if lang == "cn" else searcher_system_prompt_en
            ),
        ),
        template=dict(
            input=(
                searcher_input_template_cn
                if lang == "cn"
                else searcher_input_template_en
            ),
            context=(
                searcher_context_template_cn
                if lang == "cn"
                else searcher_context_template_en
            ),
        ),
    ),
    finance_searcher_cfg=dict(
        llm=llm,
        template=dict(
            input=(
                searcher_input_template_cn
                if lang == "cn"
                else searcher_input_template_en
            ),
            context=(
                searcher_context_template_cn
                if lang == "cn"
                else searcher_context_template_en
            ),
        ),
        plugin_executor=ActionExecutor(
            ActionYahooFinance(),
        ),
        protocol=MindSearchProtocol(
            meta_prompt=datetime.now().strftime("The current date is %Y-%m-%d."),
            plugin_prompt=(
                finance_system_prompt_cn if lang == "cn" else finance_system_prompt_en
            ),
        ),
    ),
    news_searcher_cfg=dict(
        llm=llm,
        template=dict(
            input=(
                searcher_input_template_cn
                if lang == "cn"
                else searcher_input_template_en
            ),
            context=(
                searcher_context_template_cn
                if lang == "cn"
                else searcher_context_template_en
            ),
        ),
        plugin_executor=ActionExecutor(
            ActionGNewsAPI(api_key=API_KEYS["gnews"]),
        ),
        protocol=MindSearchProtocol(
            meta_prompt=datetime.now().strftime("The current date is %Y-%m-%d."),
            plugin_prompt=(
                News_system_prompt_cn if lang == "cn" else News_system_prompt_en
            ),
        ),
    ),
    max_turn=10,
)

# 初始化数组 A[0..1500]
A = [None] * 1501
A[0] = '''你需要综合运用searcher,Finance,News工具完成以下单项选择题,最终回复明确选项,如1.A .你一定需要将题目和选项都作为root_node的content,避免遗漏信息.
在response节点中需要明确指出你的答案，如1.A  格式为题号：选项 不要输出具体该选项内容.
请注意,当Finance,News都未查询到相关数据时,也有可能用searcher中查询到.
请注意WebSearchGraph类已经存在，请不要重新定义或from import,直接运用即可。
'''

# 打开并读取文本文件
with open('assets/question.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 初始化变量
current_question = ''
question_number = 1

# 定义正则表达式模式
pattern_question_number = re.compile(r'^\d+\.\s*')  
pattern_option = re.compile(r'^[A-E]\.')        

# 遍历所有行
for line in lines:
    text = line.strip()
    
    # 检查是否是新的题目编号
    if pattern_question_number.match(text):
        # 如果已经有当前问题，先保存到数组中
        if current_question != '':
            A[question_number] = current_question.strip()
            question_number += 1
            current_question = ''
            if question_number > 1500:
                break
        # 开始新的问题
        current_question += text + '\n'
    
    # 检查是否是选项部分
    elif pattern_option.match(text) or text == '选项：':
        current_question += text + '\n'
    
    # 其他内容也添加到当前问题
    else:
        current_question += text + '\n'

# 保存最后一个问题
if current_question != '' and question_number <= 1500:
    A[question_number] = current_question.strip()

# 打开一个文件用于写入答案
with open('assets/answers.txt', 'w', encoding='utf-8') as f:
    for i in trange(1,11,desc="Question"):
        max_retries = 3  
        for attempt in range(1, max_retries + 1):
            try:
                for agent_return in agent.stream_chat(A[0] + '\n' + A[i]):
                    pass  
                answer = re.findall(r'[A-E]', agent_return.response)
                if not answer:
                    answer = agent_return.response
                    f.write(A[i] + "\n") 
                    f.write(f"{i}. {answer}\n")
                else:
                    answer = answer[-1]
                    f.write(f"{i}. {answer}\n")
                    print("Success")
                break  # 成功，跳出重试循环
            except Exception as e:
                print(f"第 {i} 题处理出现错误: {e}，尝试第 {attempt} 次。")
                if attempt < max_retries:
                    wait_time =  attempt
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)  
                else:
                    f.write(f"第 {i} 题处理失败，跳过。")
                    
