import pymysql

class MysqlConn():
    def __init__(self, user, host, password, port, db):
        self.conn = pymysql.connect(
            user=user, host=host, password=password, port=port, db=db)
        self.c = self.conn.cursor()

class MysqlOpt():
    def __init__(self, db, tbname):
        self.db = db
        self.tbname = tbname

