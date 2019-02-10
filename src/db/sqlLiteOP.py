#!/usr/bin/python3
# _*_ coding: utf-8 _*_

'''
test
the simple options of sqllite database 
''' 
import dbClass
import sys
import os
#import ..comm
#print (sys.path);
#print(__name__)
myPath = os.path.abspath('..');
sys.path.append(myPath);
import comm
#import "/home/Dr/coder/spider.py/src/comm.py"
#import ..comm

dbName = "spider.db";

db = dbClass.sqliteOp(dbName);

tableInfo = dbClass.dbTable("website");
tableInfo.insertEle({'url':'char(50)', 'null':False, 'default':' '});
tableInfo.insertEle({'pre_web':'char(50)', 'null':True});
tableInfo.insertEle({'createTime':'datetime','null':False, 'default':'0000-00-00 00:00:00'});

#print(tableInfo.showEle());
#print(tableInfo.createStr());
#createStr = tableInfo.createStr();
#print(createStr);
#db.createTable(tableInfo);
#db.createTable(createStr);

webTemp = comm.webInfo('www.baidu.com', 'www.baidu2.com');
webTemp2 = dbClass.dateWeb();
webTemp2.__dict__ = webTemp.__dict__;
#print(webTemp2.insertStr(tableInfo));
insertStr = webTemp2.insertStr(tableInfo);
#db.insertDate(webTemp2,tableInfo);
for i in range(5):
    db.insertDate(insertStr);

del db;
