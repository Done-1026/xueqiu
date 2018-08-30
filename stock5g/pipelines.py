# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql

from Utils.mysql_api import MysqlConn,MysqlOpt

logging.basicConfig(level=logging.INFO)


class StockInfoPipeline(object):

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        logging.info((self.host, self.port, self.user, self.password, self.database))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.conn_db = MysqlConn(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.conn_tb_info = MysqlOpt(self.conn_db, 'info')


    def close_spider(self, spider):
        self.conn_db.close()

    def process_item(self, item, spider):
        try:
            self.conn_db.c.execute('insert into info values {0}'.format(tuple(item.values())))
            return item
        except pymysql.err.IntegrityError as e:
            logging.info('<'+item['name']+'>'+'该公司信息已存在!')


class StockBaseLinksPipeline(StockInfoPipeline):

    def open_spider(self, spider):
        self.conn_db = MysqlConn(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.conn_tb_info = MysqlOpt(self.conn_db, 'info')
        self.conn_tb_links = MysqlOpt(self.conn_db, 'base_link')
        spider.conn_tb_info = self.conn_tb_info

    def process_item(self, item, spider):
        link = item['links']
        link.pop(-3)
        self.conn_tb_links.insert(args=link)
        #return item
