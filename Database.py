#import cx_Oracle
#print('次卧')
#table = 'V_TB_YKT_ZFB'
#connectObj = cx_Oracle.connect("sys/oracle@47.100.215.222:1521/orcl",mode=cx_Oracle.SYSDBA)
#conn = cx_Oracle.connect("用户名/密码@服务器地址/服务器名")


# -*- coding:utf-8 -*-
import cx_Oracle



os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'


class Oracle:
    def __init__(self):
        self.str = "sys/oracle@47.100.215.222:1521/orcl"
        self.cursor = None
        self.isClosed = True
        self.conn = None

    # oracle connected or not
    def isOpen(self):
        if self.cursor is not None:
            return True
        else:
            return False

    # oracle connect
    def open(self):
        try:
            self.conn = cx_Oracle.connect(self.str, mode=cx_Oracle.SYSDBA)
            self.cursor = cx_Oracle.Cursor(self.conn)
            self.isClosed = False

        except Exception as e:
            print('连接出错')
            self.cursor = None
            self.isClosed = True

        return self.cursor

    # close oracle connect
    def close(self):
        self.cursor.close()
        self.conn.close()
        self.isClosed = True

    # execute SQL
    # return:
    #       None: error
    #       empty list: 0 result
    #       normal list: normal result, a list of tuples
    def executeSQL(self, sql):
        if not self.isOpen():
            conn = self.open()
            if not self.isOpen():
                return None
        else:
            conn = self.cursor
        try:
            r = conn.execute(sql)
            sqlRes = r.fetchall()
        except Exception as e:
            print('执行语句错误')
            return None
        return sqlRes




if __name__ =='__main__':
    b = Oracle()
    b.open()
    re = b.executeSQL('select  * from V_TB_YKT_ZFB where rownum<=10 order by ssje desc')
    for hang in re:
        for lie in hang:
            print(lie)


