#!/usr/bin/python3
# _*_ coding: utf-8 _*_

"""
日志等级（level）    描述
DEBUG    最详细的日志信息，典型应用场景是 问题诊断
INFO    信息详细程度仅次于DEBUG，通常只记录关键节点信息，用于确认一切都是按照我们预期的那样进行工作
WARNING    当某些不期望的事情发生时记录的信息（如，磁盘可用空间较低），但是此时应用程序还是正常运行的
ERROR    由于一个更严重的问题导致某些功能不能正常运行时记录的信息
CRITICAL    当发生严重错误，导致应用程序不能继续运行时记录的信息
"""
 
import logging
import logging.config
# 读取日志配置文件内容
logging.config.fileConfig('./sbin/logging.conf')

# 创建一个日志器logger
logger = logging.getLogger('spider')

# 日志输出
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message') 
