#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import os;
import hashlib

from log.myLog import myLog

class webInfo():
    def __init__(self, url="", pre="", depth=1, title='', summary=''):
        self.url = url;
        self.preUrl= pre;
        self.depth = depth;
        self.title = title;
        self.summary = summary;

def pathIsExist(path):
    if os.path.exists(path):
        print ("file path is exist.")
        return True;
    else:
        print ("file path is not exist.")
        return False;

def getMd5Code(info):
    m = hashlib.md5();
    m.update(info.encode('utf-8'));
    return m.hexdigest()[8:-8];

def fileReadable(path):
    if os.access("/file/path/foo.txt", os.R_OK):
        print ("File is accessible to read")
    else:
        print ("File is not accessible to read")

log = None;
logStatus = False;
def initLog(logReal, logFile="spider.log", logLevel=5):
    global log, logStatus;
    logStatus = logReal
    if logStatus:
        log = myLog(logStatus, logFile, logLevel);

def printLog(msg, level):
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

if __name__ == "__main__":
    initLog(True)
    printLog("test", "ERROR")
