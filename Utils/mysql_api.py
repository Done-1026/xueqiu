import pymysql


class MysqlConn:
    # 创建数据库连接
    def __init__(self, host, port, user, password, db):
        self.conn = pymysql.connect(
            host=host, port=port, user=user, password=password, db=db)
        self.c = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()


class MysqlOpt:
    # 创建表连接
    def __init__(self, db, tbname):
        self.db = db
        self.tbname = tbname

    @staticmethod
    def tf_dict(kw):
        # 将字典转换为SQL,where语句的条件
        term = []
        for k, v in kw.items():
            if isinstance(v, int):
                term.append(k+'='+str(v))
            else:
                term.append(k+'='+"'"+v+"'")
        return ' and '.join(term)

    def select(self, *tags, **kw):
        # 返回查询结果，tags为查询的字段，kw为查询条件
        if not tags:
            tags = '*'
        if not kw:
            self.db.c.execute("select {0} from {1}".format(','.join(tags), self.tbname))
        else:
            cond = self.tf_dict(kw)
            self.db.c.execute(
                "select {0} from {1} where {2}".format(','.join(tags), self.tbname, cond))
        result = self.db.c.fetchall()
        return result


if __name__ == '__main__':
    db = MysqlConn('localhost', 3306, 'yxd', '12345679', 'stock')
    tb = MysqlOpt(db, 'info')
    data = tb.select('name','type',type=11)
