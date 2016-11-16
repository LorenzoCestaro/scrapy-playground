from scrapy import signals
from scrapy.exporters import CsvItemExporter
import logging


class CsvExportPipeline(object):

    def __init__(self):
        self.outputs = dict()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_closed(self, spider):
        for output in self.outputs:
            self.outputs[output]['exporter'].finish_exporting()
            self.outputs[output]['file'].close()

    def process_item(self, item, spider):
        url = item['url']
        domain = url.split('/')[2]
        filename = 'data/%s.csv' % domain

        if filename not in self.outputs:
            self.outputs[filename] = {}
            f = open(filename, 'w+')
            exporter = CsvItemExporter(f)
            self.outputs[filename]['file'] = open(filename, 'w+')
            self.outputs[filename]['exporter'] = exporter
            exporter.start_exporting()

        self.outputs[filename]['exporter'].export_item(item)
        return item
