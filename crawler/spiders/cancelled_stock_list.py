from crawler.items import StockInfo
import scrapy
import json


class CancelledStockListSpider(scrapy.Spider):
    name = 'cancelled_stock_ist'
    allowed_domains = ['hsx.vn']
    start_urls = [
        'https://www.hsx.vn/Modules/Listed/Web/CancelledStockList?y=2021&rows=30&page=1&sidx=id&sord=desc']

    def parse(self, response):
        data = json.loads(response.body)
        rows = data['rows']
        for row in rows:
            item = StockInfo()
            cell = row['cell']
            item['link'] = cell[1]
            item['symbol'] = cell[2]
            item['title'] = cell[4]
            item['date'] = cell[5]
            item['value'] = cell[6]
            yield item
