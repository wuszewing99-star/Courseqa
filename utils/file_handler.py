# utils/file_handler.py

import json
import os

from utils.logger import logger


def read_json_file(file_path):
    """
    读取 JSON 文件。

    如果文件不存在，返回空列表。
    如果 JSON 格式错误，记录 error 日志，并返回空列表。
    """

    try:
        # 文件不存在，说明还没有历史记录
        if not os.path.exists(file_path):
            logger.warning(f"JSON 文件不存在，返回空列表：{file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info(f"成功读取 JSON 文件：{file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败：{file_path}，错误：{e}")
        return []

    except Exception as e:
        logger.error(f"读取 JSON 文件失败：{file_path}，错误：{e}")
        return []


def write_json_file(file_path, data):
    """
    写入 JSON 文件。

    如果目录不存在，自动创建目录。
    写入时使用 ensure_ascii=False，避免中文乱码。
    """

    try:
        folder = os.path.dirname(file_path)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

        logger.info(f"成功写入 JSON 文件：{file_path}")
        return True

    except Exception as e:
        logger.error(f"写入 JSON 文件失败：{file_path}，错误：{e}")
        return False


def read_text_file(file_path):
    """
    读取普通文本文件。
    主要用于读取 Markdown 文档。
    """

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        logger.error(f"读取文本文件失败：{file_path}，错误：{e}")
        return ""
