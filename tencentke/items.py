# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

TENCENTKE_ITEM_PATH = 'ke.qq'

class TencentkeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    prefix_path = scrapy.Field()
    url = scrapy.Field()
    key = scrapy.Field()
    iv = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    m3u8_url = scrapy.Field()
    ts_urls = scrapy.Field()
    ts_files = scrapy.Field()
    content = scrapy.Field()

class M3u8Item(scrapy.Item):
    prefix_path = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    proxy = scrapy.Field()
    ts_name = scrapy.Field()
