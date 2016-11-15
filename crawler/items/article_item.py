from scrapy.item import Item, Field


class ArticleItem(Item):
    url = Field()
    content = Field()
