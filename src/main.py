#!/usr/bin/python3
#coding:utf-8

import sys
import os
#import traceback
import queue
import threading

from spiderList.listOpt import spiderList
from crawl.URLManager import UrlManager
from crawl.HtmlDownloader import HtmlDownloader
from crawl.HtmlParser import HtmlParser
from db.DataOutput import DataOutput
from log.myLog import myLog
from comm import initLog,webInfo,printLog, getMd5Code
#from comm import *
#import time
'''
>>> import comm
'''

CONF_PATH = "../sbin/conf.ini";

threadLock = threading.Lock();

class WorkManager():
    '''
    线程管理类
    '''
    def __init__(self, thread_num=10):
        self.work_queue = queue.Queue()
        self.threads = []
        self.__init_thread_pool(thread_num)
    
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(WorkThread(self.work_queue))

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()

    def start_allThread(self):
        for item in self.threads:
            item.start();

class WorkThread(threading.Thread):
    '''
    运行线程类
    '''
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        #self.start()
        #self.lock = lock
#
    def run(self):
        while True:
            try:
                #print_time(self.name, self.counter, 3)
                do, args = self.work_queue.get(block=False)
                #threadLock.acquire()
                do(args)
                manager = args[0];
                if manager.tree_size() <= manager.crawl_size:
                    break;
                #threadLock.release()
                self.work_queue.task_done()
            except:
                printLog("workThread except error:" + str(sys.exc_info()), "ERROR")
                #break
        printLog("workThread (%s) is finised" %self.name, "INFO")


def crawl(args):
    '''
     args = [manager, downloader, parser, depth_max, workM,     "webroot"];
    '''
    if args is None:
        printLog("crawl param is none", "ERROR")


    printLog(str(args), "DEBUG")
    manager = args[0];
    downloader = args[1];
    parser = args[2];
    depth_max = args[3]
    workM = args[4]
    url_id = args[5];

    try:
        #从URL管理器获取新的url
        url, pre_url, depth= manager.get_urlInfo_withID(url_id)
        manager.add_old_url(url_id);
        #HTML下载器下载网页
        html = downloader.download(url);
        
        if html is None:
            return
        #HTML解析器抽取网页数据
        new_urls,data = parser.parser(url,html)

        #将抽取到url添加到URL管理器中
        if new_urls is None or len(new_urls) == 0:
            pass;
        else:
            if data['match']:
                webInfoTmp = webInfo(url, pre_url, depth, data['title'], data['summary'])
                output.store_data(webInfoTmp)

            if depth < depth_max:
                for new_url in new_urls:
                    new_id = getMd5Code(new_url) 
                    if manager.add_new_url(new_url, url_id=new_id, parent=url_id):
                        workM.add_job(crawl, manager, downloader, parser, depth_max, workM, new_id) 
        
        printLog("已经爬取%s个链接"%manager.old_url_size(), "INFO")
    except Exception as e:
        printLog("crawl exception error (%s) :%s" %(url,e), "FATAL")
        return
    except:
        printLog( "crawl error:%s" %sys.exc_info(), "CRITICAL")


if __name__ == "__main__":
    listTmp = spiderList(CONF_PATH);
    options = listTmp.options;

    logStatus = True;
    logPath = "spider.log"
    if options.logpath is None:
        logStatus = False;
        pass;
    else:
        logPath = options.logpath
    
    if options.testself:
        if int(options.loglevel) > 3:
            os.system("python3 -m doctest -v ./test.py")
            #doctest.testmod(verbose=True);
        else:
            os.system("python3 -m doctest ./test.py")
            #doctest.testmod();

    initLog(logStatus, logPath, int(options.loglevel))
    printLog(str(options), "INFO");

    downloader = HtmlDownloader();
    parser = HtmlParser(options.key);
    output = DataOutput();
    depth_max = int(options.depth);
    manager = UrlManager(options.url, depth_max);
    workM = WorkManager(int(options.nthread));
    printLog("spider main is init successed", "INFO")

    args = [manager, downloader, parser, depth_max, workM, "webroot"];
    crawl(args);

    workM.start_allThread();
    workM.wait_allcomplete();

    manager.outputTree2file();
    printLog("spider is finished", "INFO")
