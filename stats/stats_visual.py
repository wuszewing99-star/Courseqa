import plotly.graph_objects as go
import pandas as pd

def visualize_history():
    # 直接造测试数据，强制弹出图表！
    daily_df = pd.DataFrame({
        "date": ["2025-05-01", "2025-05-02", "2025-05-03"],
        "count": [5, 3, 8]
    })

    top_df = pd.DataFrame({
        "question": ["什么是Python", "循环怎么写", "列表是什么"],
        "count": [5, 3, 2]
    })

    subject_df = pd.DataFrame({
        "subject": ["Python", "数学", "英语"],
        "count": [10, 5, 3]
    })

    # 柱状图
    fig_daily = go.Figure(go.Bar(x=daily_df["date"], y=daily_df["count"]))
    fig_daily.update_layout(title="每日提问量统计（升级任务）")
    fig_daily.show()

    # TOP 条形图
    fig_top10 = go.Figure(go.Bar(x=top_df["count"], y=top_df["question"], orientation="h"))
    fig_top10.update_layout(title="TOP5 高频问题")
    fig_top10.show()

    # 饼图
    fig_pie = go.Figure(go.Pie(labels=subject_df["subject"], values=subject_df["count"]))
    fig_pie.update_layout(title="科目分类（饼图）")
    fig_pie.show()

    # 环形图
    fig_ring = go.Figure(go.Pie(labels=subject_df["subject"], values=subject_df["count"], hole=0.4))
    fig_ring.update_layout(title="科目分类（环形图）")
    fig_ring.show()

if __name__ == "__main__":
    visualize_history()