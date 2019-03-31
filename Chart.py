#coding:utf-8
from flask import Flask, render_template,request
import cx_Oracle
import os
from decimal import Decimal
import datetime
import sys
import json



os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'



#生成Flask实例
app = Flask(__name__)


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

    def execute(self, sql, v1, v2):
        if not self.isOpen():
            conn = self.open()
            if not self.isOpen():
                return None
        else:
            conn = self.cursor
        try:
            r = conn.execute(sql, (v1, v2))
            sqlRes = r.fetchall()
        except Exception as e:
            print('执行语句错误')
            return None
        return sqlRes

#默认返回当天的数据
#也可以通过http://127.0.0.1:5000/top10/xxxx-xx-xx访问特定某天的数据

def show_top10(day = datetime.date.today()):
#在浏览器上渲染表格模板
    db = Oracle()
    db.open()
    sql = "select * from"\
          "(select * from" \
          "(select xfzxm,xgh,ssje,zzjg,jysj from V_TB_YKT_ZFB where jysj like '%s%s') " \
            "order by ssje desc) where rownum <=10" % (str(day), '%')
    re = db.executeSQL(sql)
    db.close()
    cost_list = []
    for row in re:
        cost_list.append(str(Decimal(row[2]).quantize(Decimal('0.00'))/100))
    #return render_template('top.html', re=re, list=cost_list)
    return [re, cost_list]


def analysis(day = datetime.date.today()):
    day = str(day)
    db = Oracle()
    #db.open()
    sql = "select count(*) from (select * from V_TB_YKT_ZFB where jysj like '%s%s')where ssje>{0} and ssje<{1}" % \
          (day, '%')
    list = [['0', '100'], ['100', '500'], ['500', '1000'], ['1000', '2000'], ['2000', '5000'], ['5000', '10000'],
            ['10000', str(sys.maxsize)]]
    re = []
    for rows in list:
        temp = sql.format(str(rows[0]), str(rows[1]))
        #print(temp)
        re.append(db.executeSQL(temp)[0])
    lanmu = ['大于100', '50-100', '20-50', '10-20', '5-10', '1-5', '0-1']
    return [re, lanmu]


def weekanalysis(date=datetime.date.today()):
    week_date = []
    #xinqi = []
    date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
    week_date.insert(0, str(date))
    for i in range(6):
        week_date.insert(0, str(date+datetime.timedelta(days=-i-1)))
    db = Oracle()
    re = []
    sql = "select sum(ssje) from V_TB_YKT_ZFB  where jysj like '{0}{1}'"
    for row in week_date:
        temp = sql.format(row, '%')
        value=db.executeSQL(temp)[0][0]
        if value==None:
            value = 0
        value = Decimal(value).quantize(Decimal('0.00'))/100
        re.append(int(value))
    return [week_date,re]

@app.route('/')
@app.route('/<date>')
def show(date=str(datetime.date.today())):

    return render_template("top.html", week=weekanalysis(date), top10=show_top10(date),qujian=analysis(date),date=date)

















if __name__ == "__main__":
    #运行项目
    app.run(debug=True,port=12345)
