#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import os;
import hashlib

from log.myLog import myLog

class webInfo():
    '''
    网页信息类，用于存储网页的页面信息
    '''
    def __init__(self, url="", pre="", depth=1, title='', summary=''):
        self.url = url;
        self.preUrl= pre;
        self.depth = depth;
        self.title = title;
        self.summary = summary;

def pathIsExist(path):
    '''
    检测文件路径上的文件是否存在
    param: filepath
    return: True or False
    '''
    if os.path.exists(path):
        printLog("file path is exist.")
        return True;
    else:
        printLog("file path is not exist.")
        return False;

def getMd5Code(info):
    '''
    获取字符串的md5加密码
    为了减轻内存负担，故取中间16位数
    param: data
    return: md5 code [8:-8]

    >>> getMd5Code('1111')
    '196a4758191e42f7'
    '''
    m = hashlib.md5();
    m.update(info.encode('utf-8'));
    return m.hexdigest()[8:-8];

def fileReadable(path):
    '''
    检测文件的可读性与否
    param: path
    return True or false
    '''
    if os.access("/file/path/foo.txt", os.R_OK):
        printLog("File is accessible to read")
        return True;
    else:
        printLog("File is not accessible to read")
        return False;

log = None;
logStatus = False;
def initLog(logReal, logFile="spider.log", logLevel=5):
    '''
    初始化记录日志的类，通用性
    '''
    global log, logStatus;
    logStatus = logReal
    if logStatus:
        log = myLog(logStatus, logFile, logLevel);

def printLog(msg, level="INFO"):
    '''
    日志输出接口增加通用性
    >>> printLog("test", "ERROR")
    ERROR test
    >>> initLog(True)
    >>> printLog("test", "ERROR")
    '''
    if log is None:
        print(level + " " + msg);
    else:
        log.printLog(msg, level);
'''
if logStatus:
    print("log");
    def printLog(msg, level):
        log.printLog(msg, level);
else :
    print("print");
    def printLog(msg, level):
        print(level + " " + msg);
'''

def testSelf():
    import doctest
    doctest.testmod(verbose=True);

if __name__ == "__main__":
    testSelf()
