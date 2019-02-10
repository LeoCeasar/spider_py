#!/usr/bin/python3
# _*_ coding: utf-8 _*_
 
import sys
from treelib import Node, Tree
import threading

sys.path.append("..");
from comm import printLog,getMd5Code

def clearFile(path):
    '''
    清空文档内容
    param: path
    return:
    '''
    f=open(path,'w');
    f.truncate()
    f.close()


class TimeThread(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        #self.start()
        #self.lock = lock
        #
    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                do(args)
                manager = args[0];
                if manager.tree_size() <= manager.crawl_size:
                    break;
                #threadLock.release()
                self.work_queue.task_done()
            except:
                #break
                printLog("TimeThread (%s) is finised" %self.name, "INFO")

            

class UrlManager(object):
    '''
    url 管理类
    '''
    def __init__(self, initUrl, depth=2):
        self.urlTree = Tree();
        self.urlTree.create_node(initUrl, "webroot");
        self.depth = depth;
        self.new_ids = set();
        self.new_ids.add('webroot');
        self.old_ids = set();
        self.treeFile = "tree.txt";
        self.crawl_size = 0;#测试使用数据
        self.url_timer();
        printLog("UrlManager init successed", "INFO");

                           
    def has_new_url(self):
        '''
        判断是否有未爬取的url
        return: True or False
        '''
        return self.new_url_size()!=0

    def get_new_urlid(self):
        '''
        获取一个未爬取的URL ID
        return: id
        '''
        url_id = self.new_ids.pop();
        self.old_ids.add(url_id);
        return url_id;

    def get_urlInfo_withID(self, url_id):
        '''
        根据id获取一个未爬取的URL info
        param:id
        return: url preurl depth
        '''
        url = self.urlTree[url_id].tag;
        pre_id = self.urlTree[url_id].bpointer;
        pre_url = None;
        if pre_id is not None:
            pre_url = self.urlTree[pre_id].tag;
        depth = self.urlTree.level(url_id);
        return url,pre_url,depth

    def get_new_url(self):
        '''
        获取一个未爬取的URL
        在单线程中使用，于多线程中废弃
        '''
        pre_id = self.new_ids.pop();
        
        new_url = self.urlTree[pre_id].tag;
        pre_url = self.urlTree[pre_id].bpointer;
        depth = self.urlTree.level(pre_id);

        self.old_ids.add(new_id);
        return new_url, pre_url, depth, new_id;

    def add_old_url(self, url_id):
        '''
        队列中添加已经获取过的URL ID
        '''
        if url_id is None:
            return False;
        self.old_ids.add(url_id);
        self.crawl_size = self.crawl_size + 1;
        return True;

    def add_new_url(self, url, url_id =None, parent = None):
        '''
        将新的url添加到未爬取的url集合中
        :param url:单个url
        :return
        '''
        if url is None:
            printLog("add new url:url param is none", "CRITICAL")
            return False;

        new_id = 0;
        if url_id is None:
            new_id = getMd5Code(url);
        else:
            new_id = url_id;

        printLog("%s url_id:%s" %(url, new_id), "DEBUG");
        try:
            if new_id not in self.new_ids and new_id not in self.old_ids:
                if parent is None:
                    self.urlTree.create_node(url, new_id);
                else:
                    self.urlTree.create_node(url, new_id, parent=parent);
            #self.new_ids.add(new_id);
                printLog("%s url add succeed" %url, "INFO")
                return True;
            else:
                printLog("%s url is repeated" %url, "DEBUG")
                return False;
        except:
            printLog("add new error:%s" %sys.exc_info(), "ERROR")

    def add_new_urls(self, urls, parent=None):
        '''
        将新的url集合添加到未爬取的url集合中
        :param urls:url 集合
        :return:
        '''
        if urls is None or len(urls) == 0:
            return False;
        for url in urls:
            self.add_new_url(url, parent);

    def new_url_size(self):
        '''
        获取未爬取的url集合的大小
        :return:
        '''
        return len(self.new_ids);

    def old_url_size(self):
        '''
        获取已经爬取的url集合的大小
        :return:
        '''
        return len(self.old_ids);
    def tree_size(self):
        '''
        url 树的大小
        return: url tree size
        '''
        return self.urlTree.size();

    def outputTree2file(self):
        '''
        将树结构输出到文本文件中
        用于测试使用
        '''
        clearFile(self.treeFile)
        self.urlTree.save2file(self.treeFile);
        printLog("treefile(%s) is output" %self.treeFile, "INFO")

    def url_timer(self):
        '''
        定时输出，简单实现
        '''
        print("成功爬取(%s/%s)个url，共需爬取%s个" %(self.old_url_size(), self.crawl_size, self.tree_size()));
        print('当前线程数为{}'.format(threading.activeCount()));
        if self.tree_size() > self.old_url_size():
            t=threading.Timer(10,self.url_timer)
            t.start()

