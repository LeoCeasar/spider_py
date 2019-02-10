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
>>> from spiderList.listOpt import spiderList
"""
