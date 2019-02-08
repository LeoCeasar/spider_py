#!/usr/bin/python3
# _*_ coding: utf-8 _*_
'''
the self.parser for command line option
'''
     
#import optparse
import configparser
import sys
from optparse import OptionParser

sys.path.append("..");
import comm;
    
class spiderList():
    def __init__(self, confPath="../../sbin/conf.ini"):

        '''
        '''
        '''
        #if not pathIsExist(path):
        try:
            self.config.read(confPath);
        except FileNotFoundError as e:
            print ("conf.ini is not fount,use the default configuration.("+e+")");
        except PersmissionError as e:
            print ("don't have the permission to access conf.ini,use the default configuration.("+e+")");
        except KeyError as e:
            print ("the conf.ini don\'t have the key of \"spider\".use default configuration.("+e+")");
        except :
            sys.exit();
        '''

        self.config = configparser.ConfigParser();
        self.config.read(confPath);
    
        self.hStr = '%prog ' + self.config['spider']['version'];
        self.desStr = 'a tool which can transform date from website';
        
        self.parser = OptionParser(self.hStr,description=self.desStr, version=self.hStr)
        
        if self.config['spider']['url'] is None:
            self.parser.add_option('-u', '--url', action='store', dest='url', help='the website url which you want to get dates from', default='sina.com.cn');
        else:
            self.parser.add_option('-u', '--url', action='store', dest='url', help='the website url which you want to get dates from', default=self.config['spider']['url']);
        
        if self.config['spider']['depth'] is None:
            self.parser.add_option('-d','--depth', action='store', default=3, dest='depth', help='the depth of website you want to get');
        else:
            self.parser.add_option('-d','--depth', action='store', default=self.config['spider']['depth'], dest='depth', help='the depth of website you want to get');
        
        if self.config['spider']['thread'] is None:
            self.parser.add_option('-t', '--thread', action='store', dest='nthread', default=10, help='the num of thread to get date from website');
        else:
            self.parser.add_option('-t', '--thread', action='store', dest='nthread', default=self.config['spider']['thread'], help='the num of thread to get date from website');
        
        if self.config['spider']['dbfile'] is None:
            self.parser.add_option('-b', '--dbfile', action='store', dest='dbpath', default='./spider.db', help='the datebase file path url ,you need to stoer the date from url');
        else:
            self.parser.add_option('-b', '--dbfile', action='store', dest='dbpath', default=self.config['spider']['dbfile'], help='the datebase file path url ,you need to stoer the date from url');
        
        self.parser.add_option('-k', '--key', action='store', dest='key', help='hte key words of website');
        
        self.parser.add_option('-l', '--logfile', action='store', dest='logpath', help='the log file');

        if self.config['spider']['loglevel'] is None:
            self.parser.add_option('--loglevel', action='store', default=1, help='the log level (1-5)');
        else:
            self.parser.add_option('--loglevel', action='store', default=self.config['spider']['loglevel'], help='the log level (1-5)');
        '''
        if self.config['spider']['logfile'] is None:
            self.parser.add_option('-f', '--logfile', action='store', default='./spider.log', dest='logpath', help='the log file');
        else:
            self.parser.add_option('-f', '--logfile', action='store', default=self.config['spider']['logfile'], dest='logpath', help='the log file');
        
        if self.config['spider']['loglevel'] is None:
            self.parser.add_option('-l', '--loglevel', action='store', default=1, help='the log level (1-5)');
        else:
            self.parser.add_option('-l', '--loglevel', action='store', default=self.config['spider']['loglevel'], help='the log level (1-5)');
        '''
        
        self.parser.add_option('-s', '--testself', action='store_true', dest='testself', default=False, help='do you want to test it self');
        
        (self.options, self.args) = self.parser.parse_args();
        

if __name__ == '__main__':
    mylist = spiderList();
    print(mylist.options);

