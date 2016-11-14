import scrapy


class ArticleSpider(scrapy.Spider):
    name = 'article'

    start_urls = [
        'http://www.jennstrends.com/find-best-followers-on-instagram/',
    ]

    def parse(self, response):
        for div in response.css('div.excerpt'):
            yield {'article': div.extract()}

        next_pages = response.css('.yarpp-related a::attr(href)').extract()
        print next_pages
        for page in next_pages:
            page = response.urljoin(page)
            yield scrapy.Request(page, callback=self.parse)
