import numpy as np
import json
import logging

import scrapy

from stock5g.items import GsjjItem

logging.basicConfig(level=logging.INFO)

class Gsjj(scrapy.Spider):
    name = 'gsjj'
    custom_settings = {
        'ITEM_PIPELINES':{'stock5g.pipelines.DataPipeline': 300}
    }

    def start_requests(self):
        url = r'https://xueqiu.com'
        yield scrapy.Request(url, meta={'cookiejar': 1})

    def parse(self, response):
        links = self.conn_tb_links.select('code', 'gsjj')
        for i in links:
            code, link = i
            url = r'https://xueqiu.com/stock/f10/compinfo.json'
            params = {
                'symbol': code
            }
            yield scrapy.FormRequest(
                url, formdata=params, method='GET',
                meta={'cookiejar': response.meta['cookiejar'], 'code': code}, callback=self.parse1)

    def parse1(self, response):
        item = GsjjItem()
        self.conn_tb_gsjj.select()
        tags = list(np.array(self.conn_tb_gsjj.db.c.description)[..., 0])
        #logging.info(tags)
        result = json.loads(response.text).get('tqCompInfo')
        #logging.info(result)
        datas = [response.meta['code']]
        for tag in tags[1:]:
            data = result.get(tag, False)
            if data is not False:
                if isinstance(data, (list, tuple)):
                    i = []
                    for mes in data:
                        new_mes = list(filter(None, list(mes.values())))
                        i.append(','.join(new_mes))
                    data = ';'.join(i)
                if data is None:
                    data = 'null'
                datas.append(data)
            else:
                raise Exception(tag+'数据错误！')
        #logging.info(datas)
        item['datas'] = datas
        self.conn_tb_gsjj.insert(datas)
        yield item


