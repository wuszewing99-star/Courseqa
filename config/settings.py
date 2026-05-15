# config/settings.py

import os

# ============================================================
# 1. 项目基础路径
# ============================================================

# 当前项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# data 目录
DATA_DIR = os.path.join(BASE_DIR, "data")

# Markdown 知识库目录
MD_DIR = os.path.join(DATA_DIR, "md")

# 历史记录文件
HISTORY_FILE_PATH = os.path.join(DATA_DIR, "history.json")

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, "logs")

# 日志文件
LOG_FILE_PATH = os.path.join(LOG_DIR, "courseqa.log")

# ============================================================
# 2. 检索相关配置
# ============================================================

# 默认返回前几条结果
DEFAULT_TOP_K = 5

# 返回文本片段最大长度
MAX_PREVIEW_CHARS = 200

# ============================================================
# 3. 历史记录相关配置
# ============================================================

# 最多保存多少条历史记录
MAX_HISTORY_RECORDS = 1000

# 默认标签
DEFAULT_TAG = "Python"

# ============================================================
# 4. 日志相关配置
# ============================================================

# 日志等级
LOG_LEVEL = "INFO"
