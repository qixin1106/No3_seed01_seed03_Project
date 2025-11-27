import logging
import os
from datetime import datetime

# 确保日志目录存在
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 创建日志记录器
logger = logging.getLogger("todo_app")
logger.setLevel(logging.DEBUG)

# 创建文件处理器，每天生成一个新的日志文件
log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.ERROR)  # 只记录错误及以上级别的日志

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台记录信息及以上级别的日志

# 创建日志格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_exception(exception: Exception, context: str = ""):
    """记录异常信息到日志文件"""
    logger.error(f"异常上下文: {context}")
    logger.exception(exception)


def log_info(message: str):
    """记录信息到日志文件"""
    logger.info(message)


def log_warning(message: str):
    """记录警告到日志文件"""
    logger.warning(message)
