#!/usr/bin/python3
#coding:utf-8

import re
import urllib.parse
from bs4 import BeautifulSoup
import sys

if sys.version_info[0] ==3:
    from urllib.parse import urlparse
else:
    from urllib import urlparse

sys.path.append("..");
from comm import printLog


class HtmlParser(object):
    '''
    html 解析
    '''
    def __init__(self,key=None):
        self.key = key;

    def parser(self,page_url,html_cont):
        '''
        用于解析网页内容抽取URL和数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return:返回URL和数据
        '''
        if page_url is None or html_cont is None:
            return
        printLog(page_url + " is crawlling", "INFO");
        soup = BeautifulSoup(html_cont,'html.parser')
        #python3 缺省的编码是unicode
        #soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data


    def _get_new_urls(self,page_url,soup):
        '''
        抽取新的URL集合
        :param page_url: 下载页面的URL
        :param soup:soup
        :return: 返回新的URL集合
        '''
        new_urls = set()
        #抽取符合要求的a标签
        #原书代码
        # links = soup.find_all('a',href=re.compile(r'/view/\d+\.htm'))
        #2017-07-03 更新,原因百度词条的链接形式发生改变
        links = soup.find_all('a', href=re.compile(r'.*news.sina.com.cn/.*'))
        for link in links:
            #提取href属性
            new_url = link['href']
            #拼接成完整网址
            new_full_url = urllib.parse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls
    def _get_new_data(self,page_url,soup):
        '''
        抽取有效数据
        :param page_url:下载页面的URL
        :param soup:
        :return:返回有效数据
        '''
        try:
            data={}
            data['match'] = True;

            if not urlparse(page_url).scheme:
                page_url = 'http://' + page_url;

            data['url']=page_url
            data['title'] = soup.title.string;
            #data['summary'] = soup.find('meta', {"name":"description"});
            data['summary'] = soup.find('div',class_="keywords");
            if data['title'] is None:
                data['title']=''
            if data['summary'] is not None:
                data['summary'] = data['summary'].get("data-wbkey");
                #data['summary'] = data['summary'].get("content");
            else:
                data['summary']='';

            if self.key is not None:
                if self.key not in data['title'] and self.key not in data['summary']:
                    data['match'] = False;

            #printLog("title:%s is crawlled" %data['title'], "INFO")
            return data
        except:
            printLog("get new data error:%s" %str(sys.exc_info()), "ERROR")
            if data['title'] is None:
                data['title']="";
            if data['summary'] is None:
                data['summary']=""
            if self.key is not None:
                if self.key not in data['title'] and self.key not in data['summary']:
                    data['match'] = False;

            return data

if __name__ == "__main__":
    from urllib.request import urlopen,Request
    from urllib.parse import urlparse
    import ssl
    import requests

    url = sys.argv[1];
    key = sys.argv[2];
    parser = HtmlParser(key)
    ssl._create_default_https_context = ssl._create_unverified_context
    if not urlparse(url).scheme:
        url = 'http://' + url;

    #req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    #html = urlopen(req).read()
#print(urlopen(req).read())
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent':user_agent, 'Connection': 'close',}
    r = requests.get(url,headers=headers)
    r.encoding='utf-8'
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    #print(soup.prettify());
    new_urls, data = parser.parser(url, html)
    #print(html);
    if data['match']:
    #print(new_urls)
        print(data);
