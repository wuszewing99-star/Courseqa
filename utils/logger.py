# utils/logger.py

import logging
import os

from config.settings import LOG_DIR, LOG_FILE_PATH, LOG_LEVEL

# ============================================================
# 1. 确保日志目录存在
# ============================================================

os.makedirs(LOG_DIR, exist_ok=True)

# ============================================================
# 2. 创建项目统一使用的 logger
# ============================================================

logger = logging.getLogger("courseqa")

# ============================================================
# 3. 设置日志等级
# ============================================================

logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# ============================================================
# 4. 避免重复添加 handler
# ============================================================
# 说明：
# uvicorn --reload 时，Python 文件可能被重新加载。
# 如果不判断 logger.handlers，可能会重复添加多个日志输出器，
# 导致同一条日志被打印多次。

if not logger.handlers:

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    # 写入日志文件
    file_handler = logging.FileHandler(
        LOG_FILE_PATH,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # 同时输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 添加到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
