#!/usr/bin/python3
#coding:utf-8

import sys
from list.listOpt import spiderList

from crawl.URLManager import UrlManager
from crawl.HtmlDownloader import HtmlDownloader
from crawl.HtmlParser import HtmlParser
from db.DataOutput import DataOutput
from log.myLog import myLog
from comm import initLog,webInfo,printLog
#from comm import *

CONF_PATH = "../sbin/conf.ini";

class SpiderMan(object):
    #def __init__(self, initUrl, depth=2, logStatus=True, logFile="spider.log", logLevel=5):
    def __init__(self, initUrl, depth=2, logStatus=True):
        self.downloader = HtmlDownloader();
        self.parser = HtmlParser();
        self.output = DataOutput();
        self.depth = 0;
        self.depth  = depth;
        self.manager = UrlManager(initUrl, depth);
        #printLog = myLog(logStatus, logFile, logLevel);
        
    def crawl(self):
    #def crawl(self,root_url):
        #添加入口URL
        #self.manager.add_new_url(root_url,self.depth)
        #判断url管理器中是否有新的url，同时判断抓取了多少个url
        #while(self.manager.has_new_url() and self.manager.old_url_size()<100):
        while(self.manager.has_new_url()):
            try:
                #从URL管理器获取新的url
                new_url, pre_url, depth, new_id = self.manager.get_new_url()
                #HTML下载器下载网页
                html = self.downloader.download(new_url)
                if html is None:
                    printLog("html error page:" + new_url, "ERROR");
                    continue;
                #HTML解析器抽取网页数据
                new_urls,data = self.parser.parser(new_url,html)
                #将抽取到url添加到URL管理器中
                if depth < self.depth:
                    self.manager.add_new_urls(new_urls, new_id)
                #数据存储器储存文件
                #if data is not None:
                    #self.output.store_data(data)
                webInfoTmp = webInfo(new_url, depth, data)
                self.output.store_data(webInfoTmp)
                printLog("已经抓取%s个链接"%self.manager.old_url_size(), "INFO")
            except Exception as e:
                printLog("crawl failed", "FATAL");
                printLog(str(e), "FATAL")
                break;
            #数据存储器将文件输出成指定格式
        self.manager.outputTree2file();
        #self.output.output_html()

if __name__=="__main__":
    listTmp = spiderList(CONF_PATH);
    print(listTmp.options);
    logStatus = True;
    logPath = "spider.log"
    if listTmp.options.logpath is None:
        logStatus = False;
        pass
    else:
        logPath = listTmp.options.logpath

    initLog(logStatus, logPath, int(listTmp.options.loglevel))
    spider_man = SpiderMan(listTmp.options.url,
            int(listTmp.options.depth))
    '''
    spider_man = SpiderMan(listTmp.options.url,
            int(listTmp.options.depth), 
            logStatus,
            logPath,
            int(listTmp.options.loglevel));
    '''
    spider_man.crawl();
    #spider_man.crawl(listTmp.options.url);
