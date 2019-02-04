#!/usr/bin/python3
# _*_ coding: utf-8 _*_
 
class UrlManager(object):
    def __init__(self) :
        self.new_urls = set();
        self.old_urls = set();

    def has_new_url(self):
        '''
        判断是否有未爬取的url
        '''
        return self.new_url_size()!=0

    def get_new_url(self):
        '''
        获取一个未爬取的URL
        '''
        new_url = self.new_urls.pop();
        self.old_urls.add(new_url);
        return new_url;

    def add_new_url(self, url):
        '''
        将新的url添加到未爬取的url集合中
        :param url:单个url
        :return
        '''
        if url is None:
            return False;
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url);

    def add_new_urls(self,urls):
        '''
        将新的url集合添加到未爬取的url集合中
        :param urls:url 集合
        :return:
        '''
        if urls is None or len(urls) == 0:
            return False;
        for url in urls:
            self.add_new_url(url);

    def new_url_size(self):
        '''
        获取未爬取的url集合的大小
        :return:
        '''
        return len(self.new_urls);

    def old_url_size(self):
        '''
        获取已经爬取的url集合的大小
        :return:
        '''
        return len(self.old_urls);
