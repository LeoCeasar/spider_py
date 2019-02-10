#python3 -m doctest ./testDoc.py

"""
>>> from comm import getMd5Code,printLog,initLog,pathIsExist
>>> getMd5Code('1111')
'196a4758191e42f7'
>>> confPath = "../sbin/conf.ini"
>>> pathIsExist(confPath)
INFO file path is exist.
True
>>> printLog("test", "ERROR")
ERROR test
>>> initLog(True)
>>> printLog("test", "ERROR")
>>> from list.listOpt import spiderList
>>> mylist = spiderList(confPath);
>>> print(mylist.options);
{'url': 'sina.com.cn', 'depth': '2', 'nthread': '10', 'dbpath': 'spider.db', 'key': None, 'logpath': None, 'loglevel': '1', 'testself': False}
"""
