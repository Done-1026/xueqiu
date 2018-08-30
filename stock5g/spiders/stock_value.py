import logging

import pymysql
import scrapy

from Utils.mysql_api import MysqlConn, MysqlOpt
from stock5g.items import StockBasicLinksItem

logging.basicConfig(level=logging.INFO)


class StockValue(scrapy.Spider):
    name = 'stock_value'
    custom_settings = {
        'ITEM_PIPELINES':{'stock5g.pipelines.StockBaseLinksPipeline': 400}
    }

    def start_requests(self):
        for i in self.conn_tb_info.select('code', 'name', type=11):
            code, name = i
            url = 'https://xueqiu.com/S/'+code
            headers = {
                'referer': 'https://xueqiu.com/k?q='+name
            }
            yield scrapy.Request(url, headers=headers,meta={'code': code, 'name': name})

    def parse(self, response):
        item = StockBasicLinksItem()
        code_name = [response.meta['code'], response.meta['name']]
        links = response.xpath(r"//div[@class='stock-links']//li//a//@href").extract()
        print(response.request.headers['User-Agent'])
        links.pop(-3)
        item['links'] = code_name+links
        #logging.info(item)
        return item

