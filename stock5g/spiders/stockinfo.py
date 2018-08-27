import random
import csv
import json

import scrapy

from Utils import util_settings as us

class StockInfo(scrapy.Spider):
    name = 'stock_info'
    with open('companys.csv','r') as f:
        comps = list(csv.reader(f))
        #print(comps)

    def start_requests(self):
        url = r'https://xueqiu.com'
        headers = {
            'User-Agent': random.choice(us.MY_USER_AGENTS),
            'Host': 'xueqiu.com',
        }
        yield scrapy.Request(url,headers=headers,meta={'cookiejar':1})

    def parse(self, response):
        cookies = response.headers.getlist(b'Set-Cookie')
        print(cookies)
        with open('companys.csv', 'r') as f:
            comps = list(csv.reader(f))
        for comp in comps[0]:
            url = r'https://xueqiu.com/stock/search.json'
            referer = r'https://xueqiu.com/k?q=' + comp
            headers = {
                'User-Agent': random.choice(us.MY_USER_AGENTS),
                'Host': 'xueqiu.com',
                'Referer': referer,
                'Cookie': cookies
            }
            params = {
                'code': comp
            }
            yield scrapy.Request(url, headers=headers,body=json.dumps(params),
                                 callback=self.parse1)

    def parse1(self, response):
        print(response.status)
