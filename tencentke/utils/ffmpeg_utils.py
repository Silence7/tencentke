#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import codecs
import os
import re
import m3u8

class TSAction(object):
    file_path = ''
    name = ''

    def __init__(self, file_path ,name):
        self.file_path = file_path
        self.name = name

    def get_m3u8_file(self):
        return '{0}/{1}.m3u8'.format(self.file_path, self.name)

    def get_ts_file(self):
        return '{0}/{1}.txt'.format(self.file_path, self.name)

    def get_video(self):
        return '{0}/{1}.mp4'.format(self.file_path, self.name)

    def check_ts_files(self):
        ''' 检查ts文件是否完整
        '''
        pass

    def merge_ts_files(self):
        ''' 合并ts文件为mp4
        '''
        # ffmpeg -f concat -i 610005-1.txt -c copy output.mp4
        cmd = 'ffmpeg -f concat -i "{0}" -c copy "{1}"'.format(self.get_ts_file(), self.get_video())
        res = os.popen(cmd).read()
        print(res)
        return True

    def remove_ts_files(self):
        '''删除ts文件
        '''
        cmd = 'rm -rf "{}"/*.ts'.format(self.file_path)
        res = os.popen(cmd).read()
        print(res)

        cmd = 'rm -rf "{}"'.format(self.get_m3u8_file())
        res = os.popen(cmd).read()
        print(res)

        cmd = 'rm -rf "{}"'.format(self.get_ts_file())
        res = os.popen(cmd).read()
        print(res)

class TencentKeTSAction(TSAction):
    def __init__(self, file_path, name):
        super(TencentKeTSAction, self).__init__(file_path, name)

    def check_ts_files(self):
        files = os.listdir(self.file_path)
        with codecs.open(self.get_m3u8_file(), 'r', encoding='utf-8') as file:
            extstr = file.read()
            extobj = m3u8.parse(extstr)
            for segment in extobj['segments']:
                uri = segment['uri']
                ts_name = uri.split('?')[0]
                if ts_name not in files:
                    return False

            return True
            