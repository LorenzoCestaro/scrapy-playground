from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate url found: %s" % item['url'])
        else:
            self.ids_seen.add(item['url'])
            return item
