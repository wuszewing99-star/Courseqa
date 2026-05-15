# ============================================================
# api/stats_api.py
# 统计接口模块
# ============================================================
#
# 本文件用于定义 CourseQA 系统的统计接口：/stats。
#
# 需要注意：
# 1. 如果只是本地运行统计图表，例如：
#       python -m stats.stats_visual
#    那么程序会直接读取 data/history.json，
#    调用 stats/history_stats.py 中的统计函数生成 DataFrame，
#    然后由 stats/stats_visual.py 使用 Plotly 直接绘图。
#    这种情况下，不会经过本文件中的 /stats 接口。
#
# 2. 本文件主要在以下场景中使用：
#    - 浏览器访问：
#        http://127.0.0.1:8000/stats
#    - 前端页面通过 AJAX / fetch 请求统计数据
#    - 其他程序通过 HTTP 请求获取统计结果
#
# 3. 本文件的核心作用是：
#    - 读取 data/history.json 中的历史记录
#    - 调用 stats/history_stats.py 中的统计函数
#    - 得到 pandas DataFrame 格式的统计结果
#    - 使用 .to_dict(orient="records") 将 DataFrame 转成
#      可通过 HTTP 返回的 JSON 结构
#
# 简单理解：
#    stats_visual.py 负责“本地画图”
#    stats_api.py    负责“对外提供统计接口数据”
#
# 数据流程：
#    data/history.json
#        ↓
#    stats/history_stats.py 统计生成 DataFrame
#        ↓
#    api/stats_api.py 转换为 JSON
#        ↓
#    浏览器 / 前端 / 其他程序访问 /stats 获取统计结果
# ============================================================
from fastapi import APIRouter
from stats.history_stats import load_flat_history, get_daily_counts, get_top_questions, get_subject_counts

stats_router = APIRouter()

@stats_router.get("/stats")
def stats_summary():
    history = load_flat_history()
    return {
        "total_questions": len(history),
        "daily_counts": get_daily_counts(history).to_dict(orient="records"),
        "top10_questions": get_top_questions(history).to_dict(orient="records"),
        "subject_counts": get_subject_counts(history).to_dict(orient="records")
    }