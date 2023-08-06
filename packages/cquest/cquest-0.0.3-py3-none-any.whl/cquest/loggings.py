import logging.config
import os

import yaml

from cquest import root_dir

# 读取日志配置文件yaml
with open(os.path.join(root_dir, 'loggings.yaml'), 'r', encoding='utf-8') as f:
    source = yaml.safe_load(f)
    source['handlers']['file_all']['filename'] = 'all.log'
    source['handlers']['file_error']['filename'] = 'error.log'

# 将日志配置内容转换为字典
logging.config.dictConfig(source)

# 创建一个日志器
logger = logging.getLogger('CCP')

# 按级别执行对象
"""
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

logging.StreamHandler	将日志消息发送到输出到Stream，如std.out, std.err或任何file-like对象。
logging.FileHandler	将日志消息发送到磁盘文件，默认情况下文件大小会无限增长
logging.handlers.RotatingFileHandler	将日志消息发送到磁盘文件，并支持日志文件按大小切割
logging.handlers.TimedRotatingFileHandler	将日志消息发送到磁盘文件，并支持日志文件按时间切割
logging.handlers.HTTPHandler	将日志消息以GET或POST的方式发送给一个HTTP服务器
logging.handlers.SMTPHandler	将日志消息发送给一个指定的email地址
"""
