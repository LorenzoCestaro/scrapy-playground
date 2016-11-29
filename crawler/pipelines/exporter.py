from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import logging
import os
from parsetools import utils
import re


class TxtExportPipeline(object):
    def open_spider(self, spider):
        filename = '/tmp/data/%s.txt' % spider.name
        self.out = open(filename, 'a')

    def close_spider(self, spider):
        self.out.close()

    def process_item(self, item, spider):
        # Basic html preprocessing
        text = item['content']
        regex = re.compile(ur'[^\x00-\x7F]+', re.UNICODE)
        text = re.sub(regex, ' ', text)
        text = re.sub('[\n\t\r]', ' ', text)

        # Text extraction with bs4
        text = BeautifulSoup(text, 'lxml')
        for script in text(['script', 'style']):
            script.extract()

        text = text.get_text()
        text = utils.clean(text)

        # Save to file
        self.out.write(text + '\n')

        return item
