"""
@Date    : 2024/11/23
@Author  : YueJiang
@File    : log_config.py
@Software: PyCharm  
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from consts.config_vars import LOG_FILE

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE)
p = os.path.abspath(os.path.dirname(log_file))
if not os.path.exists(p):
    os.makedirs(p)
logger_apscheduler = logging.getLogger('apscheduler.executors.default')
logger_apscheduler.setLevel(logging.WARNING)

# 创建一个 RotatingFileHandler，最多备份10个日志文件，单个日志文件最大10MB
handler = logging.handlers.RotatingFileHandler(filename=str(log_file), maxBytes=100 * 1024 * 1024, backupCount=10)
handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter(
    '%(name)s [p%(process)d_t%(thread)d] %(asctime)s %(filename)s:%(lineno)d [%(levelname)s] - %(message)s',
    "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
