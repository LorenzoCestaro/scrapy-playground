import scrapy
from crawler.items.article import ArticleItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = [
        'socialmedia.biz',
        'www.leveragesocialmedia.com',
    ]

    start_urls = [
        'http://www.socialmedia.biz/',
        'http://www.leveragesocialmedia.com/',
    ]

    def parse(self, response):
        for article in response.css('article'):
            item = ArticleItem()
            item['url'] = response.url
            item['content'] = article.extract()
            yield item

        next_pages = response.css('body a::attr(href)').extract()
        for page in next_pages:
            page = response.urljoin(page)
            yield scrapy.Request(page, callback=self.parse)
