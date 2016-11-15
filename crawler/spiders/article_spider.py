import scrapy
from crawler.items import ArticleItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['rebekahradice.com']

    start_urls = [
        'http://rebekahradice.com/blog/',
    ]

    def parse(self, response):
        for article in response.css('body article'):
            item = ArticleItem()
            item['url'] = response.url
            item['content'] = article
            yield item

        next_pages = response.css('body a::attr(href)').extract()
        for page in next_pages:
            page = response.urljoin(page)
            yield scrapy.Request(page, callback=self.parse)
