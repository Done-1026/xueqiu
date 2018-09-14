import logging

import pymysql

logging.basicConfig(level=logging.INFO)


class MysqlConn:
    """
    创建一个mysql数据库连接,数据库必须已被创建
    """
    def __init__(self, host, port, user, password, database):
        self.conn = pymysql.connect(
            host=host, port=port, user=user, password=password, database=database)
        self.c = self.conn.cursor()

    def close(self, save=True):
        # 断开连接，save参数判定是否保存，默认保存
        fun = lambda: {'Y': self.conn.commit, 'N': fun}.get(input("是否保存修改(Y/N)"))
        if save:
            self.conn.commit()
        self.conn.close()

    def commit(self):
        # 提交已执行的操作
        self.conn.commit()


class MysqlOpt:
    """在库连接基础上，创建表连接"""
    def __init__(self, db, tbname):
        self.db = db
        self.tbname = tbname

    def __len__(self):
        return self.db.c.execute("desc %s" % self.tbname)

    @staticmethod
    def trf_dict(kw):
        """将字典转换为SQL,where语句的条件"""
        term = []
        for k, v in kw.items():
            if isinstance(v, int):
                term.append(k + '=' + str(v))
            else:
                term.append(k + '=' + "'" + v + "'")
        return ' and '.join(term)

    def get_tags(self):
        """查询表的创建"""
        self.db.c.execute("desc %s" % self.tbname)
        return self.db.c.fetchall()

    def select(self, *tags, **kw):
        """返回查询结果，tags为查询的字段，kw为查询条件"""
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

    def insert(self, values, tags=tuple()):
        """info
        插入一条记录
        tags  插入数据的字段，元组或列表，不传时，为插入所有字段
        values  插入的数据，元组或列表
        * 插入单字段数据时，必须以（data,）的形势插入，括号中的逗号是必须的
        """
        if not isinstance(tags, (tuple, list)) or not isinstance(values, (tuple, list)):
            raise Exception('Error: type error, must be tuple or list!')
        tags = '(' + ','.join(tags) + ')'
        values = tuple(values) if len(values) > 1 else str(values)[:-2] + ')'
        sentence = "insert into {0} {1} values {2}".format(self.tbname, tags, values)
        logging.info('SQL sentence > " %s "]' % sentence)
        try:
            self.db.c.execute(sentence)
            self.db.commit()
        except pymysql.err.ProgrammingError as e1:
            print('Error:  ', e1)
        except pymysql.err.IntegrityError as e2:
            print('Error:  ', e2)


if __name__ == '__main__':
    db = MysqlConn('localhost', 3306, 'yxd', '12345679', 'stock')
    tb = MysqlOpt(db, 'info')
    # a = tb.select()
