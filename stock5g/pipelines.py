# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql

logging.basicConfig(level=logging.INFO)


class StockInfoPipeline(object):

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        logging.info((self.host, self.port, self.user, self.password, self.db))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, user=self.user,
                                    password=self.password, port=self.port, database=self.db)
        self.c = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.c.execute('insert into info values {0}'.format(tuple(item.values())))
            return item
        except pymysql.err.IntegrityError as e:
            logging.info('<'+item['name']+'>'+'该公司信息已存在!')


