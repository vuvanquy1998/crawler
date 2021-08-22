# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from os import scandir
import scrapy


class StockInfo(scrapy.Item):
    date = scrapy.Field()
    value = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    symbol = scrapy.Field()
