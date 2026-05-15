# ============================================================
# history_stats.py
# ============================================================
#
# 本文件用于 CourseQA 项目历史记录统计
#
# 功能：
# 1. 读取 history.json 中保存的用户历史查询记录
# 2. 按不同统计维度生成 pandas DataFrame
#    - 每日提问量统计
#    - TopN 高频问题统计
#    - 各科目分类统计
#
# 生成的 DataFrame 可直接用于 Plotly 绘图或进一步分析
# ============================================================

import json
import pandas as pd
from pathlib import Path
from collections import Counter
from datetime import datetime

# 定义历史记录文件路径
HISTORY_FILE = Path("data/history.json")


def load_flat_history():
    """
    读取最新格式的历史记录列表

    返回：
        list: 历史记录，每个元素是一个字典
    """
    # 如果历史记录文件不存在，返回空列表
    if not HISTORY_FILE.exists():
        return []

    try:
        # 打开文件并读取 JSON 内容
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception as e:
        # 如果读取或解析失败，打印错误并返回空列表
        print(f"读取历史失败: {e}")
        return []

    # 返回读取到的历史记录列表
    return history


def get_daily_counts(history):
    """
    按天统计每日提问量

    参数：
        history (list): 历史记录列表，每条记录包含 time 字段

    返回：
        pd.DataFrame: 两列 DataFrame，date 表示日期，count 表示该天提问次数
    """
    # 从每条历史记录中截取日期部分 YYYY-MM-DD
    dates = [record["time"][:10] for record in history]

    # 使用 Counter 统计每天出现次数
    counter = Counter(dates)

    # 将统计结果转换为 DataFrame，并按照日期排序
    df = pd.DataFrame(sorted(counter.items()), columns=["date", "count"])
    return df


def get_top_questions(history, top_n=10):
    """
    统计 TopN 高频问题

    参数：
        history (list): 历史记录列表，每条记录包含 query 字段
        top_n (int): 返回出现次数最多的前 N 个问题

    返回：
        pd.DataFrame: 两列 DataFrame，question 表示问题文本，count 表示出现次数
    """
    # 提取每条记录中的 query 字段
    queries = [record["query"] for record in history]

    # 使用 Counter 统计每个 query 出现次数
    counter = Counter(queries)

    # 获取出现次数最多的 top_n 个问题
    df = pd.DataFrame(counter.most_common(top_n), columns=["question", "count"])
    return df


def get_subject_counts(history):
    """
    统计各科目分布

    参数：
        history (list): 历史记录列表，每条记录包含 tag 字段

    返回：
        pd.DataFrame: 两列 DataFrame，subject 表示科目名称，count 表示该科目出现次数
    """
    # 提取每条记录的 tag 字段，如果没有 tag 则标记为 "未知"
    tags = [record.get("tag", "未知") for record in history]

    # 使用 Counter 统计每个科目出现次数
    counter = Counter(tags)

    # 转换为 DataFrame
    df = pd.DataFrame(counter.items(), columns=["subject", "count"])
    return df