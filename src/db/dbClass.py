#!/usr/bin/python3
# _*_ coding: utf-8 _*_
 
import sqlite3;
import types;
import os
import sys

#myPath = os.path.abspath("..");
sys.path.append("..");
from comm import printLog,webInfo
'''
数据库相关类，用于数据库的输出
预计可以实现结构化的数据库输出
中途发现构思存在缺陷。未实现完全
'''

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
        '''
        根据insertEle 里面传输的元素信息，进行数据库构建语句的字符串拼接
        '''
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

    def showEle(self):
        return self.ele;

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

    '''
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
    '''

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
        '''
        增加数据
        一开始想和创建数据库表的时候一样进行结构化的数据库语句拼接，
        后发现容易引发数据库的安全问题，故改善
        '''
        try :
            with sqlite3.connect(self.dbName) as con:
                cur = con.cursor();
                if isinstance(webData, webInfo):
                    sql = "insert into " +tableInfo.tableName+ "(url, pre_url, depth, title, summary) values (?,?,?,?,?)"
                    para = (webData.url, webData.preUrl, webData.depth, webData.title, webData.summary)
                    cur.execute(sql, para);
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
