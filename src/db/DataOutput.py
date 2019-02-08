#!/usr/bin/python3
# _*_ coding: utf-8 _*_
 
import codecs

from .dbClass import *

class DataOutput(object):
    def __init__(self) :
        dbName = "spider.db";
        self.db = sqliteOp(dbName);
        #self.db = dbClass.sqliteOp(dbName);

        self.tableInfo = dbTable("website");
        self.tableInfo.insertEle({'url':'varchar', 'null':False, 'default':' '});
        self.tableInfo.insertEle({'pre_url':'varchar', 'null':True});
        self.tableInfo.insertEle({'depth':'int(2)','null':False, 'default':'0'});
        self.tableInfo.insertEle({'title':'int(2)','null':True, 'default':'0'});
        self.tableInfo.insertEle({'summary':'text','null':True, 'default':'0'});
        self.db.createTable(self.tableInfo);
        #self.data = dataWeb();
        #self.data = dbClass.dataWeb();
        
        #self.datas = [];

    def store_data(self, data):
        if data is None:
            return
        '''
        webTmp = dataWeb();
        webTmp.__dict__ = data.__dict__;
        '''
        self.db.insertData(data, self.tableInfo)
        #self.db.insertData(webTmp, self.tableInfo)
        #self.datas.append(data);
        
