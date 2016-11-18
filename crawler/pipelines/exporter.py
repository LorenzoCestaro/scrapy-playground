# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exporters import CsvItemExporter
import logging
import os
from parsetools import html_parse
import re


class TxtExportPipeline(object):

    def __init__(self):
        self.outputs = dict()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_closed(self, spider):
        for path, filename in self.outputs.iteritems():
            filename.close()
            html_parse.parse(path=path, clean=True)
            os.remove(path)

    def process_item(self, item, spider):
        url = item['url']
        domain = url.split('/')[2]
        filename = 'data/%s.txt' % domain

        if filename not in self.outputs:
            self.outputs[filename] = open(filename, 'w+')\

        text = item['content'].encode('ascii', 'ignore')
        text = re.sub('[\n\t\r]', '', text)
        text = re.sub('<article', '\n<article', text)

        self.outputs[filename].write(text)
        return item
