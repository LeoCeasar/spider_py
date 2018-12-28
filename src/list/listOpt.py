#!/usr/bin/python3
# _*_ coding: utf-8 _*_
'''
the parser for command line options
'''
 
#import optparse
import configparser
import sys
from optparse import OptionParser

config = configparser.ConfigParser();
config.read("../../sbin/conf.ini");

hStr = '%prog ' + config['spider']['version'];
desStr = 'a tool which can transform date from website';

parser = OptionParser(hStr,description=desStr, version=hStr)

parser.add_option('-u', '--url', action='store', dest='url', help='the website url which you want to get dates from');
parser.add_option('-d','--depth', action='store', default=3, dest='depth', help='the depth of website you want to get');
parser.add_option('-t', '--thread', action='store', dest='nthread', default=10, help='the num of thread to get date from website');
parser.add_option('-b', '--dbfile', action='store', dest='dbpath', default='./spider.db', help='the datebase file path url ,you need to stoer the date from url');
parser.add_option('-k', '--key', action='store', dest='key', help='hte key words of website');
parser.add_option('-f', '--logfile', action='store', default='./spider.log', dest='logpath', help='the log file');
parser.add_option('-l', '--loglevel', action='store', default=1, help='the log level (1-5)');
parser.add_option('-s', '--testself', action='store_true', dest='testself', default=False, help='do you want to test it self');

(options, args) = parser.parse_args();

print(options);
