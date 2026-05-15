import os
import re
import json
from pathlib import Path
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config.settings import MD_DIR, MAX_PREVIEW_CHARS
from utils.file_handler import read_text_file
from utils.logger import logger


HISTORY_FILE = Path("data/history.json")


def read_markdown_documents(md_dir=MD_DIR):
    """
    读取 data/md/ 目录下的所有 Markdown 文件。
    返回：
    [
        {
            "doc": "lesson1.md",
            "text": "文档内容"
        },
        ...
    ]
    """
    documents = []

    if not os.path.exists(md_dir):
        logger.error(f"Markdown 目录不存在：{md_dir}")
        return documents

    for filename in os.listdir(md_dir):

        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(md_dir, filename)
        text = read_text_file(file_path)

        if text.strip():
            documents.append({
                "doc": filename,
                "text": text
            })

    logger.info(f"成功读取 Markdown 文档数量：{len(documents)}")
    return documents


def split_into_chunks(documents):
    """
    将 Markdown 文档按空行切分为多个文本块。
    返回：
    [
        {
            "doc": "lesson1.md",
            "pid": 1,
            "text": "第一段内容"
        },
        ...
    ]
    """
    chunks = []

    for doc in documents:
        doc_name = doc["doc"]
        text = doc["text"]

        # 按一个或多个空行切分
        paragraphs = re.split(r"\n\s*\n+", text)

        pid = 1

        for paragraph in paragraphs:
            paragraph = paragraph.strip()

            if not paragraph:
                continue

            chunks.append({
                "doc": doc_name,
                "pid": pid,
                "text": paragraph
            })

            pid += 1

    logger.info(f"成功切分文本块数量：{len(chunks)}")
    return chunks


def build_tfidf_index(chunks):
    """
    构建 TF-IDF 索引。
    返回：
    vectorizer, tfidf_matrix
    """
    if not chunks:
        logger.warning("chunks 为空，无法构建 TF-IDF 索引")
        return None, None

    texts = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    logger.info("TF-IDF 索引构建完成")
    return vectorizer, tfidf_matrix


def shorten_text(text, max_chars=MAX_PREVIEW_CHARS):
    """
    截断文本，避免接口返回内容过长。
    """
    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "..."


def search_tfidf(query, vectorizer, tfidf_matrix, chunks, top_k):
    """
    使用 TF-IDF 执行检索。
    """
    if vectorizer is None or tfidf_matrix is None:
        raise ValueError("TF-IDF 索引未加载")

    query = query.strip()

    if not query:
        raise ValueError("query 不能为空")

    if top_k <= 0:
        raise ValueError("top_k 必须大于 0")

    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    top_k = min(top_k, len(chunks))
    top_indices = scores.argsort()[-top_k:][::-1]

    hits = []

    for index in top_indices:
        chunk = chunks[index]

        hits.append({
            "score": float(scores[index]),
            "doc": chunk["doc"],
            "pid": chunk["pid"],
            "text": shorten_text(chunk["text"])
        })

    logger.info(f"TF-IDF 查询完成，返回 {len(hits)} 条结果")
    return hits


# ------------------- 新增函数 -------------------

def save_history(question, subject, hits):
    """
    保存查询历史到 data/history.json
    统一格式：
    {
      "timestamp": "...",
      "question": "...",
      "subject": "...",
      "hits": [ {"score":..., "doc":..., "pid":..., "text":...} ]
    }
    """
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "subject": subject,
        "hits": hits
    }

    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"读取历史文件失败: {e}")
            history = []
    else:
        history = []

    history.append(record)

    try:
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"历史记录已保存: {question}")
    except Exception as e:
        logger.error(f"保存历史失败: {e}")