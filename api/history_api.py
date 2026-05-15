# api/history_api.py

from config.settings import (
    HISTORY_FILE_PATH,
    MAX_HISTORY_RECORDS,
    DEFAULT_TAG
)
from utils.file_handler import read_json_file, write_json_file
from utils.time_utils import get_current_time, parse_time
from utils.logger import logger


def get_all_history():
    """
    获取全部历史记录。
    """

    history = read_json_file(HISTORY_FILE_PATH)
    logger.info(f"获取全部历史记录，共 {len(history)} 条")
    return history


def _get_next_id(history):
    """
    生成下一条历史记录的 id。

    不直接使用 len(history)+1，
    是为了避免删除记录后 id 重复。
    """

    if not history:
        return 1

    max_id = 0

    for item in history:
        item_id = item.get("id", 0)

        if isinstance(item_id, int):
            max_id = max(max_id, item_id)

    return max_id + 1


def add_history(query, top_k, result, tag=DEFAULT_TAG):
    """
    保存一条查询历史记录。

    注意：
    CourseQA 是检索系统，
    用户输入字段叫 query，
    系统返回字段叫 hits。
    """

    query = query.strip() if query else ""

    if not query:
        logger.warning("尝试保存空 query，已忽略")
        return False

    history = read_json_file(HISTORY_FILE_PATH)

    new_record = {
        "id": _get_next_id(history),
        "query": query,
        "top_k": top_k,
        "time": get_current_time(),
        "hit_count": result.get("hit_count", 0),
        "hits": result.get("hits", []),
        "tag": tag
    }

    history.append(new_record)

    # 限制最大保存条数，避免文件无限增长
    if len(history) > MAX_HISTORY_RECORDS:
        history = history[-MAX_HISTORY_RECORDS:]

    success = write_json_file(HISTORY_FILE_PATH, history)

    if success:
        logger.info("历史记录已成功保存到 history.json")
        return True

    logger.error("历史记录保存失败")
    return False


def search_history(keyword):
    """
    按关键词查询历史记录。

    查询范围：
    1. query 字段
    2. hits 中的 text 字段
    """

    keyword = keyword.strip() if keyword else ""

    if not keyword:
        logger.warning("历史记录关键词查询失败：关键词为空")
        return []

    history = read_json_file(HISTORY_FILE_PATH)
    keyword_lower = keyword.lower()

    results = []

    for item in history:
        query = item.get("query", "").lower()

        # 先检查 query 中是否包含关键词
        if keyword_lower in query:
            results.append(item)
            continue

        # 再检查 hits 中的 text
        hits = item.get("hits", [])

        for hit in hits:
            text = hit.get("text", "").lower()

            if keyword_lower in text:
                results.append(item)
                break

    logger.info(f"历史记录关键词查询完成：{keyword}，返回 {len(results)} 条")
    return results


def filter_history_by_time(start_time, end_time):
    """
    按时间范围筛选历史记录。

    时间格式：
    2026-03-15 14:30:00
    """

    history = read_json_file(HISTORY_FILE_PATH)
    results = []

    try:
        start = parse_time(start_time)
        end = parse_time(end_time)

        for item in history:
            item_time_str = item.get("time", "")

            if not item_time_str:
                continue

            item_time = parse_time(item_time_str)

            if start <= item_time <= end:
                results.append(item)

        logger.info(
            f"历史记录时间筛选完成：{start_time} 至 {end_time}，返回 {len(results)} 条"
        )

        return results

    except Exception as e:
        logger.error(f"历史记录时间筛选失败：{e}")
        return []


def delete_history(record_id):
    """
    根据 id 删除单条历史记录。
    """

    history = read_json_file(HISTORY_FILE_PATH)

    new_history = [
        item for item in history
        if item.get("id") != record_id
    ]

    if len(new_history) == len(history):
        logger.warning(f"未找到要删除的历史记录：id={record_id}")
        return False

    success = write_json_file(HISTORY_FILE_PATH, new_history)

    if success:
        logger.info(f"已删除历史记录：id={record_id}")
        return True

    logger.error(f"删除历史记录失败：id={record_id}")
    return False


def clear_history():
    """
    清空全部历史记录。
    """

    success = write_json_file(HISTORY_FILE_PATH, [])

    if success:
        logger.info("全部历史记录已清空")
        return True

    logger.error("清空历史记录失败")
    return False
