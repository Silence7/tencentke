# -*- coding: utf-8 -*-

from abc import abstractmethod, ABCMeta
import re
import logging

import m3u8
from scrapy.selector import Selector
from tencentke.settings import FILES_STORE
from tencentke.items import VideoItem, M3u8Item, TENCENTKE_ITEM_PATH
from tencentke.utils.ffmpeg_utils import TencentKeTSAction

Logger = logging.getLogger('videoparse')

INVALID_PATTERN = 0
TENCENTKE_PATTERN = 1

TENCENTKE_HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}

INVALID_CHAR_RE = '[\r\n\t|:"" /\']'

class BaseParser(metaclass=ABCMeta):
    
    @abstractmethod
    def path(self):
        pass

    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    def proxy(self):
        pass

    @abstractmethod
    def parse_body(self, response):
        pass

    @abstractmethod
    def parse_media_url(self, response):
        pass

    @abstractmethod
    def parse_media(self, response):
        pass

    @abstractmethod
    def parse_m3u8(self, response):
        pass

    @abstractmethod
    def get_m3u8_url(self):
        pass

    @abstractmethod
    def get_m3u8_items(self):
        pass

    @abstractmethod
    def get_video_item(self):
        pass

    @abstractmethod
    def get_m3u8_action(self):
        pass

class TencentKeParser(BaseParser):
    video_item = VideoItem()
    m3u8_items = []
    
    def path(self):
        return TENCENTKE_ITEM_PATH

    def headers(self):
        return TENCENTKE_HEADERS

    def proxy(self):
        return super().proxy()

    def parse_body(self, response):
        pass 

    def parse_media_url(self, response):
        return super().parse_media_url(response)

    def parse_media(self, response):
        return super().parse_media(response)

    def parse_m3u8(self, response):
        pass

    def get_m3u8_url(self):
        return self.video_item['m3u8_url']

    def get_m3u8_items(self):
        return self.m3u8_items

    def get_video_item(self):
        return self.video_item

    def get_m3u8_action(self):
        return TencentKeTSAction(file_path='{0}/{1}/{2}/{3}'.format(FILES_STORE, self.path(), self.video_item['author'], self.video_item['title']), 
                                name=self.video_item['name'])

class BuildParser():
    
    def __init__(self):
        self.patterns = {
            re.compile(r'https://[^\s]*.ke.qq.com/[^\s]*'): TENCENTKE_PATTERN,
        }

    def search_pattern(self, string):
        for key, value in self.patterns.items():
            ret = re.search(key, string)
            if ret:
                return value

        return INVALID_PATTERN

    def build(self, url):
        pattern = self.search_pattern(url)
        
        if pattern == TENCENTKE_PATTERN:
            return TencentKeParser()

        return None