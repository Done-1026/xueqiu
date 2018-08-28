# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql

logging.basicConfig(level=logging.INFO)

class StockInfoPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='localhost', user='yxd',
                               password='12345679', port=3306, db='stock')
        self.c = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.c.execute('INSERT INTO info VALUES {0}'.format(tuple(item.values())))
            return item
        except pymysql.err.IntegrityError as e:
            logging.info('<'+item['name']+'>'+'该公司信息已存在!')


