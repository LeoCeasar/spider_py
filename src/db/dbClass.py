#!/usr/bin/python3
# _*_ coding: utf-8 _*_
 
import sqlite3;
import types;
import os
import sys

myPath = os.path.abspath("..");
sys.path.append(myPath);
import comm

class dbTable():
    tableName = None;
    ele = [];
    index = None;
    def __init__(self, name):
        self.tableName = name
    def insertEle(self, ele):
        self.ele.append(ele);
    def delTableStr(self):
        strTemp = "drop table if exists " + self.tableName;
        return strTemp;
    def createStr(self):
        strTemp = " Create table "+ self.tableName + " ( \n id integer not null primary key AUTOINCREMENT,\n";
        #strTemp = " Create table "+ self.tableName + " ( \n id int not null auto_increment primary key,\n";

        for i,val in enumerate(self.ele):
            items = list(val.items());
            strTemp += items[0][0] + " " + items[0][1]+ " ";
            if items[1][1]:
                strTemp += "null ,\n"
            else:
                strTemp +=  "not null ,\n ";
                #strTemp +=  " default " + items[2][1] + ",\n ";

        strTemp = strTemp[:-3];
        strTemp += " )";
        return strTemp;

    def seletStr(self, offset, count):
        strTemp = "select ";
        for i,val in enumerate(self.ele):
            items = list(val.items());
            strTemp += items[0][0]+",";
        strTemp = strTemp[:-1];
        strTemp += " from " + tableInfo.tableName +" " ;
        if (offset > 0 and count >0):
            strTemp += "limit "+ offset +", " + count;
        #strTemp += " orderby createTime desc"
        return strTemp;

    def showEle(self):
        return self.ele;

class dateWeb(comm.webInfo):
    url = "";
    preUrl = __init__(self):
        super().__init__();
    def insertStr(self, table):
        strTemp = "insert into "+table.tableName +" (";
        for i,val in enumerate(table.ele):
            items = list(val.items());
            strTemp += items[0][0]+","; 

        strTemp = strTemp[:-1];
        strTemp += " ) values ('" + self.url + "','" + self.preUrl + "', date('now'))";
        return strTemp;

class sqliteOp():
    dbName = None;
    conn = None;
    cur = None;

    def __init__(self, name):
        "数据库初始化"
        self.dbName = name;

        try:
            self.sqlConnect();
            self.cur = self.conn.cursor();
        except sqlite3.Error as e:
            print(e);
        else:
            print("sqlite3 database initial success");

    def __del__(self):
        "析构函数"
        del self.dbName;
        try:
            self.conn.close();
        except sqlite3.Error as e:
            print(e);
        else:
            print("DB connect closed success")

    def sqlConnect(self):
        "数据库链接"
        self.conn = sqlite3.connect(self.dbName);

    def createTable(self, tableInfo):
        "表创建"
        try:
            if isinstance(tableInfo, dbTable):
                self.cur.execute(tableInfo.delTableStr());
                self.cur.execute(tableInfo.createStr());
            else:
                self.cur.execute(tableInfo);
        except sqlite3.Error as e:		
            print(e);
        except Exception as e:
            print("Exeception: %s" % e)
        else:
            print("database create successed");

    def insertDate(self, webDate, tableInfo=None):
        "增"
        try :
            if isinstance(webDate,  comm.webInfo):
                self.cur.execute(webDate.insertStr(tableInfo));
            else:
                self.cur.execute(webDate);
            self.conn.commit();
        except sqlite3.Error as e:
             print(e);
        except Exception as e:
             print(e);
        else:
            pass;
				

    def delDate(self):
        "删"
        pass;

    def update(self):
        "改"
        pass;

    def selectDate(self, tableInfo, offset = 0, count = 0):
        "查"
        try:
            if isinstance(tableInfo,  comm.dbTable):
                self.cur.execute(tableInfo.selectStr(offset, count));
            else:
                self.cur.execute(tableInfo);
        except sqlite3.Error as e:
            print(e);
        except Exception as e:
            print(e);
        else:
            print("select from database success");

    def fetchOne(self):
        "匹配一条数据"
        return self.cur.fetchone();
    def fetchMany(self, size):
        "匹配多条数据"
        return self.cur.fetcnmany(size);

    def fetchAll(self):
        "匹配many条数据"
           return self.cur.fetchall();
