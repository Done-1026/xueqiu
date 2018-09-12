import numpy as np
import json
import logging

import scrapy

from stock5g.items import GsjjItem

logging.basicConfig(level=logging.INFO)


class Gsjj(scrapy.Spider):
    name = 'zycwzb'
    custom_settings = {
        'ITEM_PIPELINES': {'stock5g.pipelines.DataPipeline': 300}
    }

    def start_requests(self):
        url = r'https://xueqiu.com'
        yield scrapy.Request(url, meta={'cookiejar': 1})

    def parse(self, response):
        links = self.conn_tb_links.select('code', 'zycwzb')
        for i in links:
            code, link = i
            url = r'https://xueqiu.com/stock/f10/finmainindex.json'
            params = {
                'symbol': code,
                'page': '1',
                'size': '100'
            }
            yield scrapy.FormRequest(
                url, formdata=params, method='GET',
                meta={'cookiejar': response.meta['cookiejar'], 'code': code}, callback=self.parse1)

    def parse1(self, response):
        self.conn_tb_zycwzb.select()
        tags = list(np.array(self.conn_tb_zycwzb.db.c.description)[..., 0])
        # logging.info(tags)
        results = json.loads(response.text).get('list')
        for result in results:
            # logging.info(result)
            datas = [0, response.meta['code']]
            for tag in tags[2:]:
                data = result.get(tag, False)
                if data is not False:
                    if data is None:
                        data = 0
                    datas.append(data)
                else:
                    raise Exception(tag + '数据错误！')
            # logging.info(datas)
            self.conn_tb_zycwzb.insert(datas)
