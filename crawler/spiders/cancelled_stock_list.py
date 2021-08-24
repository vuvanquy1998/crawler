from logging import log
import logging
from crawler.items import StockInfo
import scrapy
import json
from datetime import date
import pymongo


class CancelledStockListSpider(scrapy.Spider):
    name = 'cancelled_stock_list'
    allowed_domains = ['hsx.vn']
    year = date.today().year
    lasted_date = ''

    def start_requests(self):

        # settings = self.settings
        # # init mongo connect
        # mongo_uri = settings['MONGO_URI']
        # mongo_db = settings['MONGO_DATABASE']
        # collection_name = settings['COLLECTION_NAME']
        # logging.info(f'setting. mongo_db: {mongo_db}. mongo_uri: {mongo_uri}')

        # self.client = pymongo.MongoClient(mongo_uri)
        # self.db = self.client[mongo_db]
        # colletion = self.db[collection_name]
    
        # # first = self.db[collection_name].find({}, { '$max: "$quantity"'})
        # count = colletion.count()
        # if count > 0 :
        #     first = colletion.find_one(sort=[("date", -1)])["date"]
        #     self.lasted_date = first

        # self.db[self.collection_name].insert(dict(items))
        url = f'https://www.hsx.vn/Modules/Listed/Web/CancelledStockList?y={self.year}&rows=30&page=1&sidx=id&sord=desc'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        logging.info(f'Handling year: {self.year},  page: {data["page"]}')

        for row in data['rows']:
            item = StockInfo()
            cell = row['cell']
            item['link'] = cell[1]
            item['symbol'] = cell[2]
            item['title'] = cell[4]
            item['date'] = self.format_date(cell[5])
            item['value'] = cell[6]
            # self.data.append(item)
            yield item
        if data['records'] == 0 and data['page'] == 1:
            return
        if data['records'] == 0:
            self.year = self.year - 1
            page = 1
        else:
            page = data['page'] + 1
        link = f'https://www.hsx.vn/Modules/Listed/Web/CancelledStockList?y={self.year}&rows=30&page={page}&sidx=id&sord=desc'
        yield scrapy.Request(link, callback=self.parse)
    def format_date(date):
        dateArr = date.split('/')
        day = dateArr[0]
        month = dateArr[1]
        year = dateArr[2]
        return f'{year}/{month}/{day}'