import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import numpy as np

# 设置Seaborn样式为白色网格
sns.set(style="whitegrid")

# 初始化列表存储题干和选项的字符数
question_lengths = []
option_lengths = []

# 读取文件内容
with open('assets/question.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 使用正则表达式分割每个题目
# 假设每道题目以数字加点开头，如 "1. "
questions = re.split(r'\n\d+\.\s+', content)
# 移除可能的空字符串
questions = [q.strip() for q in questions if q.strip()]

for q in questions:
    # 分割题干和选项
    parts = q.split('选项：')
    if len(parts) != 2:
        continue  # 跳过格式不符合的题目
    question_text = parts[0].strip()
    options_text = parts[1].strip()
    
    # 计算题干字符数
    question_length = len(question_text)
    question_lengths.append(question_length)
    
    # 提取所有选项
    options = re.findall(r'[A-D]\.\s*(.*?)\s*(?=[A-D]\.|$)', options_text, re.DOTALL)
    # 计算每个选项的字符数，并取平均
    if options:
        total_option_length = sum(len(option) for option in options)
        average_option_length = total_option_length / len(options)
        option_lengths.append(average_option_length)

# 定义绘图函数，增加step参数
def plot_distribution(data, title, filename, step=10):
    plt.figure(figsize=(12, 6))
    
    # 使用Seaborn计算核密度估计
    kde = sns.kdeplot(data, color="red", shade=False, bw_adjust=1.5)
    
    # 获取KDE数据
    x, y = kde.get_lines()[0].get_data()
    
    # 每隔step个点绘制一条虚线
    for i in range(0, len(x), step):
        plt.vlines(x=x[i], ymin=0, ymax=y[i], colors='red', linestyles='dashed', linewidth=0.5, alpha=0.5)
    
    # 重新绘制KDE曲线在最上层
    plt.plot(x, y, color="red")
    
    plt.title(title)
    plt.xlabel('Number of Characters')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

# 绘制题干字符数分布图，每隔10个点绘制一条虚线
plot_distribution(
    data=question_lengths,
    title='Distribution of Question Lengths',
    filename='question_length_distribution.png',
    step=3
)

# 绘制选项字符数分布图，每隔10个点绘制一条虚线
plot_distribution(
    data=option_lengths,
    title='Distribution of Option Lengths',
    filename='option_length_distribution.png',
    step=3
)
