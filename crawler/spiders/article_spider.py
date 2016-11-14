import scrapy


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['rebekahradice.com']

    # Breadth-First crawling
    custom_settings = {
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }

    start_urls = [
        'http://rebekahradice.com/blog/',
    ]

    def parse(self, response):
        for article in response.css('body article'):
            yield {'article': article.extract()}

        next_pages = response.css('body a::attr(href)').extract()
        for page in next_pages:
            page = response.urljoin(page)
            yield scrapy.Request(page, callback=self.parse)
