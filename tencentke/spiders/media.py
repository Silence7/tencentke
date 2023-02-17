import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, Response
from scrapy import signals
from tencentke.spiders.parse.video_parse import BuildParser
import logging

Logger = logging.getLogger('MediaSpider')


class MediaSpider(CrawlSpider):
    name = "media"
    allowed_domains = ["ke.qq.com"]
    start_urls = [
        # "http://ke.qq.com/"
        'https://ke.qq.com/course/457935/4057017518324943'
    ]

    # rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)

    # 保存视频文件信息
    ts_actions = []

    # 入口函数
    def start_requests(self):
        # 从文件读取会更方便
        for url in self.start_urls:
            Logger.info('url:{0}'.format(url))
            parser = BuildParser().build(url)
            yield Request(url, callback=self.parse_body, headers=parser.headers(), meta={'proxy': parser.proxy(), 'parser': parser})
        
    def parse_body(self, response):
        parser = response.meta['parser']
        parser.parse_body(response)

        media_url = parser.parse_media_url(response)
        if media_url is not None:
            yield Request(media_url, callback=self.parse_media, meta={'proxy': parser.proxy(), 'parser': parser})
        else:
            m3u8_url = parser.get_m3u8_url()
            if m3u8_url is not None:
                yield Request(m3u8_url, callback=self.parse_m3u8, meta={'proxy': parser.proxy(), 'parser': parser})
            else:
                Logger.error('MediaSpider {} media or m3u8 url is None'.format(response.url))

    def parse_media(self, response):
        parser = response.meta['parser']
        parser.parse_media(response)
        m3u8_url = parser.get_m3u8_url()
        yield Request(m3u8_url, callback=self.parse_m3u8, meta={'proxy': parser.proxy(), 'parser': parser})

    def parse_m3u8(self, response):
        parser = response.meta['parser']
        parser.parse_m3u8(response)

        for item in parser.get_m3u8_items():
            yield item
        
        self.ts_actions.append(parser.get_m3u8_action())
        yield parser.get_video_item()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # spider = cls()
        spider = super(MediaSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        # 每个ts文件都是异步下载，在所有任务都完成以后，需要合并ts文件
        for ts_action in self.ts_actions:
            if not ts_action.check_ts_files():
                Logger.error('check_ts_files error:{0}'.format(ts_action.file_path))
                continue

            if ts_action.merge_ts_files():
                # 删除ts
                ts_action.remove_ts_files()
