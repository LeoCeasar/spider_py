#!/usr/bin/python3
#coding:utf-8
import requests
import sys

if sys.version_info[0] ==3:
    from urllib.parse import urlparse
else:
    from urllib import urlparse

sys.path.append("..");
from comm import printLog

class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        if not urlparse(url).scheme:
                    url = 'http://' + url;

        requests.adapters.DEFAULT_RETRIES = 5  

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers={'User-Agent':user_agent, 'Connection': 'close',}
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            #r.encoding='utf-8'
            return r.text
        else:
            printLog("%s url is download failed." %url, "ERROR")
            return None

