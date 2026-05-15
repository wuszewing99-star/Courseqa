import os

from courseqa_core import (
    read_markdown_file,
    split_paragraphs,
    build_chunks,
    write_chunks_jsonl,
    search_count,
    build_tfidf,
    search_tfidf,
    print_search_results
)


def main():
    """
    第7次课主程序：
    1. 读取 Markdown 文件
    2. 切分段落
    3. 构建 chunks
    4. 写入 JSONL
    5. 构建 TF-IDF 模型
    6. 进入命令行循环问答
    """
    file_path = "data/md/example.md"
    output_path = "output/chunks.jsonl"
    top_k = 5
    preview_chars = 200

    # 1. 检查输入文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：输入文件不存在：{file_path}")
        return

    # 2. 读取 Markdown 文件
    text = read_markdown_file(file_path)
    if text is None:
        return

    # 3. 切分段落
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        print("没有切分出有效段落。")
        return

    # 4. 构建 chunks
    doc_name = os.path.basename(file_path)
    chunks = build_chunks(doc_name, paragraphs)

    # 5. 写入 JSONL
    ok = write_chunks_jsonl(doc_name, paragraphs, output_path)
    if ok:
        print(f"已生成 JSONL 文件：{output_path}")
    else:
        print("JSONL 文件生成失败。")

    # 6. 构建 TF-IDF 模型
    texts = [chunk["text"] for chunk in chunks]
    vectorizer, text_vectors = build_tfidf(texts)

    print("\ncourseqa 已启动。")
    print("请输入查询词进行检索；输入 exit 退出程序。")

    # 7. 命令行循环问答
    while True:
        query = input("\n请输入查询词：").strip()

        if query.lower() == "exit":
            print("程序结束。")
            break

        if not query:
            print("查询词不能为空，请重新输入。")
            continue

        if top_k <= 0:
            print("top_k 不合法，已恢复为默认值 5。")
            top_k = 5

        print("\n【Count 检索结果】")
        count_results = search_count(query, chunks, top_k=top_k)
        print_search_results(query, count_results, max_chars=preview_chars)

        print("\n【TF-IDF 检索结果】")
        tfidf_results = search_tfidf(query, vectorizer, text_vectors, chunks, top_k=top_k)
        print_search_results(query, tfidf_results, max_chars=preview_chars)


if __name__ == "__main__":
    main()