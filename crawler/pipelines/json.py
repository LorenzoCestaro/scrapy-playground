import json


class JsonWritePipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item.article)) + "\n"
        self.file.write(line)
        return item
