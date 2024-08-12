import scrapy


class WalmartspiderSpider(scrapy.Spider):
    name = "walmartspider"
    allowed_domains = ["walmart.com"]
    start_urls = ["https://www.walmart.com/"]

    def parse(self, response):
        pass
