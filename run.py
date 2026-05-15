import uvicorn
from stats.stats_visual import visualize_history

if __name__ == "__main__":
    print("启动 FastAPI 服务并访问 /stats 获取统计数据")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    # 可视化演示
    # visualize_history()