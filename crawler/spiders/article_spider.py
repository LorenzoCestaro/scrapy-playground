import scrapy
from crawler.items.article import ArticleItem
from scrapy.linkextractors import LinkExtractor, IGNORED_EXTENSIONS


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = [
        'socialnetworking-weblog.com',
        'blogster.com',
        'sociableblog.com',
        'networkweaving.com/blog',
        'blogs.alianzo.com/socialnetworks',
        'rotorblog.com',
    ]

    start_urls = [
        'http://www.socialnetworking-weblog.com/',
        'http://blogster.com/',
        'http://www.sociableblog.com/',
        'http://www.networkweaving.com/blog/',
        'http://blogs.alianzo.com/socialnetworks/',
        'http://www.rotorblog.com/',
    ]

    def parse(self, response):
        for article in response.css('article'):
            item = ArticleItem()
            item['url'] = response.url
            item['content'] = article.extract()
            yield item

        le = LinkExtractor(
            deny_extensions=IGNORED_EXTENSIONS,
            unique=True
        )

        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse)
