# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.stats_api import stats_router#-----11------------

from config.settings import DEFAULT_TOP_K, DEFAULT_TAG
from core.qa_engine import (
    read_markdown_documents,
    split_into_chunks,
    build_tfidf_index,
    search_tfidf
)
from api.history_api import (
    add_history,
    get_all_history,
    search_history,
    filter_history_by_time,
    delete_history,
    clear_history
)
from utils.logger import logger



# ============================================================
# 1. 创建 FastAPI 应用
# ============================================================

app = FastAPI(
    title="CourseQA API",
    description="课程问答系统：检索、历史记录、日志与异常处理",
    version="10.0"
)

app.include_router(stats_router)#---------11-------------

# ============================================================
# 2. 全局变量：保存索引状态
# ============================================================

chunks = []
tfidf_vectorizer = None
tfidf_matrix = None

# ============================================================
# 3. 请求体模型
# ============================================================

class QueryRequest(BaseModel):
    query: str
    top_k: int = DEFAULT_TOP_K
    tag: str = DEFAULT_TAG

# ============================================================
# 4. 启动时加载索引
# ============================================================

def load_index():
    """
    启动服务时预加载 Markdown 文档与 TF-IDF 索引。
    """

    global chunks, tfidf_vectorizer, tfidf_matrix

    logger.info("开始加载 CourseQA 索引")

    documents = read_markdown_documents()
    chunks = split_into_chunks(documents)
    tfidf_vectorizer, tfidf_matrix = build_tfidf_index(chunks)

    if tfidf_vectorizer is not None and tfidf_matrix is not None:
        logger.info("CourseQA 索引加载成功")
    else:
        logger.warning("CourseQA 索引加载失败或数据为空")

# 注意：
# 当执行 uvicorn app:app --reload 时，
# Python 会加载 app.py 文件。
# 这里会在文件加载时执行，提前构建索引。
load_index()

# 1. 服务启动日志
logger.info("CourseQA 服务启动成功")

# ============================================================
# 5. 通用查询函数
# ============================================================

def run_search(query_text: str, top_k: int):
    """
    通用检索函数。

    GET /query 和 POST /query 都可以调用这个函数。
    """

    if tfidf_vectorizer is None or tfidf_matrix is None:
        logger.error("索引未加载，无法执行查询")
        raise HTTPException(
            status_code=500,
            detail="索引未加载，请检查 data/md/ 目录中是否有 Markdown 文件"
        )

    query_text = query_text.strip()

    if not query_text:
        logger.warning("用户提交了空 query")
        raise HTTPException(
            status_code=400,
            detail="query 不能为空"
        )

    if top_k <= 0:
        logger.warning(f"非法 top_k：{top_k}")
        raise HTTPException(
            status_code=400,
            detail="top_k 必须是大于 0 的整数"
        )

    try:
        hits = search_tfidf(
            query=query_text,
            vectorizer=tfidf_vectorizer,
            tfidf_matrix=tfidf_matrix,
            chunks=chunks,
            top_k=top_k
        )

        # 3. 检索完成日志
        if len(hits) == 0:
            logger.warning(f"查询无结果：{query_text}")
        else:
            logger.info(f"查询完成，返回 {len(hits)} 条结果")

        return {
            "query": query_text,
            "top_k": top_k,
            "hit_count": len(hits),
            "hits": hits
        }

    except ValueError as e:
        logger.error(f"查询参数错误：{e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        logger.error(f"检索过程发生异常：{e}")
        raise HTTPException(
            status_code=500,
            detail="检索失败，请稍后重试"
        )

# ============================================================
# 6. 健康检查接口
# ============================================================

@app.get("/health")
def health():
    """
    健康检查接口。
    """

    return {
        "ok": True,
        "index_loaded": tfidf_vectorizer is not None and tfidf_matrix is not None,
        "chunk_count": len(chunks)
    }

# ============================================================
# 7. GET 查询接口
# ============================================================

@app.get("/query")
def get_query(query: str, top_k: int = DEFAULT_TOP_K):
    """
    GET 查询接口。

    示例：
    /query?query=FastAPI&top_k=3
    """

    # 2. 用户查询日志
    logger.info(f"收到用户查询：{query}")

    result = run_search(
        query_text=query,
        top_k=top_k
    )

    # 保存历史记录
    add_history(
        query=query,
        top_k=top_k,
        result=result,
        tag=DEFAULT_TAG
    )

    return result

# ============================================================
# 8. POST 查询接口
# ============================================================

@app.post("/query")
def post_query(query_request: QueryRequest):
    """
    POST 查询接口。

    请求体示例：
    {
        "query": "FastAPI 是什么？",
        "top_k": 3,
        "tag": "Python"
    }
    """

    query = query_request.query
    top_k = query_request.top_k
    tag = query_request.tag

    # 2. 用户查询日志
    logger.info(f"收到用户查询：{query}")

    result = run_search(
        query_text=query,
        top_k=top_k
    )

    # 保存历史记录
    add_history(
        query=query,
        top_k=top_k,
        result=result,
        tag=tag
    )

    return result

# ============================================================
# 9. 查看全部历史记录
# ============================================================

@app.get("/history")
def history():
    """
    查看全部历史记录。
    """

    all_history = get_all_history()

    return {
        "count": len(all_history),
        "history": all_history
    }

# ============================================================
# 10. 按关键词查询历史记录
# ============================================================

@app.get("/history/search")
def history_search(keyword: str):
    """
    按关键词查询历史记录。

    示例：
    /history/search?keyword=FastAPI
    """

    results = search_history(keyword)

    return {
        "keyword": keyword,
        "count": len(results),
        "results": results
    }

# ============================================================
# 11. 按时间筛选历史记录
# ============================================================

@app.get("/history/time")
def history_time(start_time: str, end_time: str):
    """
    按时间范围筛选历史记录。

    时间格式：
    2026-03-15 14:30:00
    """

    results = filter_history_by_time(
        start_time=start_time,
        end_time=end_time
    )

    return {
        "start_time": start_time,
        "end_time": end_time,
        "count": len(results),
        "results": results
    }

# ============================================================
# 12. 删除单条历史记录
# ============================================================

@app.delete("/history/{record_id}")
def history_delete(record_id: int):
    """
    根据 id 删除单条历史记录。
    """

    success = delete_history(record_id)

    if success:
        return {
            "message": f"历史记录 {record_id} 已删除"
        }

    raise HTTPException(
        status_code=404,
        detail="未找到该历史记录"
    )

# ============================================================
# 13. 清空全部历史记录
# ============================================================

@app.delete("/history")
def history_clear():
    """
    清空全部历史记录。
    """

    success = clear_history()

    if success:
        return {
            "message": "全部历史记录已清空"
        }

    raise HTTPException(
        status_code=500,
        detail="清空历史记录失败"
    )
