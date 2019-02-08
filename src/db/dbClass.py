#!/usr/bin/python3
# _*_ coding: utf-8 _*_
 
import sqlite3;
import types;
import os
import sys

#myPath = os.path.abspath("..");
sys.path.append("..");
from comm import printLog,webInfo

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
        printLog("create table str:%s" %strTemp, "DEBUG")
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

        printLog("select data str:"+strTrmp, "DEBUG")
        return strTemp;

    def showEle(self):
        return self.ele;

class dataWeb(webInfo):
    #url = "";
    #preUrl = "";
    def __init__(self):
        super().__init__();
    def insertStr(self, table):
        strTemp = "insert into "+table.tableName +" (";
        for i,val in enumerate(table.ele):
            items = list(val.items());
            strTemp += items[0][0]+","; 

        strTemp = strTemp[:-1];

        if self.preUrl is None:
            if self.summary is None:
                strTemp += " ) values ('" + self.url + "', null,"+ str(self.depth) +",null) ";
            else:
                strTemp += " ) values ('" + self.url + "', null,"+ str(self.depth) +",'"+ self.summary +"') ";
        else:
            if self.summary is None:
                strTemp += " ) values ('" + self.url + "','" + self.preUrl + "',"+ str(self.depth) +",null) ";
            else:
                strTemp += " ) values ('" + self.url + "','" + self.preUrl + "',"+ str(self.depth) +",'"+ self.summary +"') ";

        #strTemp += " ) values ('" + self.url + "','" + self.preUrl + "', date('now'))";
        printLog("insert data str:"+strTemp, "DEBUG")
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
            printLog("sqliteOp init sqlite3.error :%s" %e, "CRITICAL");
        except:
             printLog( "sqliteOp init Error" %sys.exc_info(), "CRITICAL")
        else:
            printLog("sqlite3 database initial success", "INFO");

    def __del__(self):
        "析构函数"
        del self.dbName;
        try:
            self.conn.close();
        except sqlite3.Error as e:
            printLog("sqliteop del sqlite3.error:" +str(e), "CRITICAL");
        except:
             printLog( str(sys.exc_info()), "ERROR")
        else:
            printLog("DB connect closed success", "INFO")

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
            printLog("createTable sqlite3.error:" + str(e), "CRITICAL");
        except Exception as e:
            printLog("createTable Exeception: %s" % e, "CRITICAL")
        except:
            printLog( "createTable error:%s" %sys.exc_info(), "CRITICAL")
        else:
            printLog("database create successed", "INFO");

    def insertData(self, webData, tableInfo=None):
        "增"
        try :
            with sqlite3.connect(self.dbName) as con:
                cur = con.cursor();
                if isinstance(webData, webInfo):
                    cur.execute(webData.insertStr(tableInfo));
                else:
                    cur.execute(webData);
                con.commit();
                #self.conn.commit();
        except sqlite3.Error as e:
            printLog("insertData sqlite3.error:%s" %e, "ERROR");
        except Exception as e:
            printLog("insertData Exception:%s" %e, "ERROR");
        except:
            printLog( "insertData error:%s" %sys.exc_info(), "ERROR")
        else:
            pass;
				

    def delData(self):
        "删"
        pass;

    def update(self):
        "改"
        pass;

    def selectData(self, tableInfo, offset = 0, count = 0):
        "查"
        try:
            if isinstance(tableInfo, dbTable):
                self.cur.execute(tableInfo.selectStr(offset, count));
            else:
                self.cur.execute(tableInfo);
        except sqlite3.Error as e:
            printLog("select sqlite3.error:%s" %e, "ERROR");
        except Exception as e:
            printLog("select exception error:%s" %e, "ERROR");
        else:
            printLog("select from database success", "INFO");

    def fetchOne(self):
        "匹配一条数据"
        return self.cur.fetchone();
    def fetchMany(self, size):
        "匹配多条数据"
        return self.cur.fetcnmany(size);

    def fetchAll(self):
        "匹配many条数据"
        return self.cur.fetchall();
