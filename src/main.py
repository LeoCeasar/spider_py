#!/usr/bin/python3
#coding:utf-8

from crawl.URLManager import UrlManager
from crawl.HtmlDownloader import HtmlDownloader
from crawl.HtmlParser import HtmlParser
from crawl.DataOutput import DataOutput

from list.listOpt import spiderList

CONF_PATH = "../sbin/conf.ini";

class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
    def crawl(self,root_url):
        #添加入口URL
        self.manager.add_new_url(root_url)
        #判断url管理器中是否有新的url，同时判断抓取了多少个url
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            try:
                #从URL管理器获取新的url
                new_url = self.manager.get_new_url()
                #HTML下载器下载网页
                html = self.downloader.download(new_url)
                #HTML解析器抽取网页数据
                new_urls,data = self.parser.parser(new_url,html)
                #将抽取到url添加到URL管理器中
                self.manager.add_new_urls(new_urls)
                #数据存储器储存文件
                self.output.store_data(data)
                print("已经抓取%s个链接"%self.manager.old_url_size())
            except Exception as e:
                print("crawl failed")
                print(e)
            #数据存储器将文件输出成指定格式
        self.output.output_html()

if __name__=="__main__":
    listTmp = spiderList(CONF_PATH);
    spider_man = SpiderMan()
    spider_man.crawl("http://baike.baidu.com/view/284853.htm")
