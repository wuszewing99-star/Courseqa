# utils/time_utils.py

from datetime import datetime


def get_current_time():
    """
    获取当前时间字符串。

    返回格式：
    2026-03-15 14:30:00
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_time(time_str):
    """
    将时间字符串转换为 datetime 对象。

    用于按时间筛选历史记录。
    """

    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
