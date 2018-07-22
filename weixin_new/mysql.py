import MySQLdb
from config import *


class mysql():
    """
    定义了个mysql的链接，和db中的redis类不同的是，我们保存到mysql中，没有在读取出来，所有定义的方法很少，也没有定义拿出来的方法

    """
    def __init__(self):
        try:
            self.sql=MySQLdb.Connect(host=Mysql_host,password=Mysql_password,user=Mysql_user,charset='utf8',database='wx')
            self.cursor=self.sql.cursor()
        except MySQLdb.MySQLError as e:
            print(e)
    def insert(self,table,data):
        keys = ', '.join(data.keys())#取data的字段名
        values = ', '.join(['%s'] * len(data.keys()))#取data对应的values个数，用占位符表示
        sql_query= 'insert into %s (%s) values (%s)' % (table, keys, values)#values嵌套了个占位符
        try:
          self.cursor.execute(sql_query, tuple(data.values()))           #因为sql_query中的values嵌套占位符，这样后的tuple元组形式填充
          self.sql.commit()      #每个操作要commit下才执行
        except MySQLdb.MySQLError as e:
            print(e)
            self.sql.rollback()#如果有错误则回滚

