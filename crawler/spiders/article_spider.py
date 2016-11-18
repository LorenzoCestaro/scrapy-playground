# -*- coding: utf-8 -*-

import scrapy
from crawler.items.article import ArticleItem
from scrapy.linkextractors import LinkExtractor, IGNORED_EXTENSIONS


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = [
        'techcrunch.com',
    ]

    start_urls = [
        'https://techcrunch.com',
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
