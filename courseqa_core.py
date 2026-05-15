import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_markdown_file(file_path):
    """
    读取 Markdown 文件内容。

    参数:
        file_path (str): Markdown 文件路径

    返回:
        str | None: 读取成功返回文件内容，失败返回 None
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None


def split_paragraphs(text):
    """
    按空行切分段落，并过滤空段落。

    参数:
        text (str): 原始文本

    返回:
        list[str]: 段落列表
    """
    paragraphs = text.split("\n\n")
    cleaned_paragraphs = []

    for p in paragraphs:
        p = p.strip()
        if p:
            cleaned_paragraphs.append(p)

    return cleaned_paragraphs


def build_chunks(doc_name, paragraphs):
    """
    将段落列表转换为 chunk 列表。

    参数:
        doc_name (str): 文档名
        paragraphs (list[str]): 段落列表

    返回:
        list[dict]: chunk 列表
    """
    chunks = []

    for pid, paragraph in enumerate(paragraphs, 1):
        chunk = {
            "doc": doc_name,
            "pid": pid,
            "text": paragraph
        }
        chunks.append(chunk)

    return chunks


def dumps_chunk(chunk):
    """
    将 Python 字典转换为 JSON 字符串。
    """
    return json.dumps(chunk, ensure_ascii=False, sort_keys=True)


def loads_chunk(json_text):
    """
    将 JSON 字符串恢复为 Python 字典。
    """
    return json.loads(json_text)


def write_chunks_jsonl(doc_name, paragraphs, output_path):
    """
    将段落列表写入 JSONL 文件。

    参数:
        doc_name (str): 文档名
        paragraphs (list[str]): 段落列表
        output_path (str): 输出文件路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        chunks = build_chunks(doc_name, paragraphs)

        with open(output_path, "w", encoding="utf-8") as file:
            for chunk in chunks:
                json_line = dumps_chunk(chunk)
                file.write(json_line + "\n")

        return True

    except Exception as e:
        print(f"写入 JSONL 文件时发生错误：{e}")
        return False


def search_count(query, chunks, top_k=5):
    """
    用最简单的“出现次数”方法进行检索。
    """
    query = query.strip()

    if not query:
        return []

    if top_k <= 0:
        top_k = 5

    results = []

    for chunk in chunks:
        text = chunk["text"]
        score = text.count(query)

        if score > 0:
            result = {
                "score": score,
                "doc": chunk["doc"],
                "pid": chunk["pid"],
                "text": chunk["text"]
            }
            results.append(result)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def build_tfidf(texts):
    """
    根据文本列表构建 TF-IDF 模型与文本向量矩阵。
    """
    vectorizer = TfidfVectorizer()
    text_vectors = vectorizer.fit_transform(texts)
    return vectorizer, text_vectors


def search_tfidf(query, vectorizer, text_vectors, chunks, top_k=5):
    """
    使用 TF-IDF + 余弦相似度进行检索。
    """
    query = query.strip()

    if not query:
        return []

    if top_k <= 0:
        top_k = 5

    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, text_vectors)[0]

    results = []
    for i, score in enumerate(similarities):
        if score > 0:
            result = {
                "score": float(score),
                "doc": chunks[i]["doc"],
                "pid": chunks[i]["pid"],
                "text": chunks[i]["text"]
            }
            results.append(result)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def shorten_text(text, max_chars=200):
    """
    将文本截断为前 max_chars 个字符，超出部分加省略号。
    """
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def print_search_results(query, results, max_chars=200):
    """
    以更友好的格式打印检索结果，并对正文做截断显示。
    """
    print("\n" + "=" * 60)
    print(f"查询词：{query}")
    print("=" * 60)

    if not results:
        print("没有找到相关结果。")
        return

    for i, item in enumerate(results, 1):
        print(f"[Top {i}] 分数：{item['score']} | 来源：{item['doc']} 第 {item['pid']} 段")
        print(shorten_text(item["text"], max_chars=max_chars))
        print("-" * 60)