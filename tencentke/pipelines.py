# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from tencentke.items import VideoItem, M3u8Item
from tencentke.settings import FILES_STORE
import os
import codecs
import json
import logging
Logger = logging.getLogger('TencentkePipeline')

class TencentkePipeline:
    def process_item(self, item, spider):
        if isinstance(item, VideoItem):
            self.save_tmp_files('{0}/{1}/{2}'.format(FILES_STORE, item['prefix_path'], item['author']), item)

        return item

    def save_tmp_files(self, base_path, item):
        file_path = '{0}/{1}'.format(base_path, str(item['title']))
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file = '{0}/{1}.m3u8'.format(file_path, str(item['name']))
        with codecs.open(file, 'w', encoding='utf-8') as f:
            f.write(item['content'])

        file = '{0}/{1}.txt'.format(file_path, str(item['name']))
        with codecs.open(file, 'w', encoding='utf-8') as f:
            for line in item['ts_files']:
                f.write(line)
        
class VideoFilesPipeline(FilesPipeline):
    
    def get_media_requests(self, item, info):
        if isinstance(item, M3u8Item):
            url = item['url']
            if url:
                yield Request(url, meta={'proxy': item['proxy'], 'prefix_path': item['prefix_path'], 'author':item['author'], 'title': item['title'], 'ts_name': item['ts_name']})

    def file_path(self, request, response=None, info=None):
        prefix_path = request.meta['prefix_path']
        author = request.meta['author']
        title = request.meta['title']
        ts_name = request.meta['ts_name']

        filename = '{0}/{1}/{2}/{3}'.format(prefix_path, author, title, ts_name)
        return filename
