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
#import logging.config
class myLog():
    '''
    日志输出管理类
    用于统一输出接口，为了兼容文本输出或者控制台输出
    但是由于统一输出之后无法定位到准确代码位置，所以需要在错误提示信息中进行较为精准的描述
    '''
    def __init__(self, logStatus=False, LogName='spider.log', logLevel=1):
        #self.status = logStatus;
        level = (6-logLevel) * 10;
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=level)
        #self.logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler(LogName)
        #formatter = logging.Formatter('%(threadName)s - %(thread)d - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(module)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def printLog(self, msg, level="DEBUG"):
        if level == "DEBUG":
            self.logger.debug(msg)
        elif level == "INFO":
            self.logger.info(msg)
        elif level == "WARN" or level == "WARNING":
            self.logger.warning(msg)
        elif level == "ERROR":
            self.logger.error(msg)
        elif level == "FATAL" or level == "CRITICAL":
            self.logger.critical(msg)
        else:
            self.logger.debug("error log type :" + msg)
        
         
'''
         self.logger.info('This is a log info')
         self.logger.debug('Debugging')
         self.logger.warning('Warning exists')
         self.logger.info('Finish')

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
'''
