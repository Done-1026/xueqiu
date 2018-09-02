import scrapy

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
                url, formdata=params, method='GET', meta = {'cookiejar': response.meta['cookiejar']}, callback=self.parse1)

    def parse1(self, response):
        print(response.text)