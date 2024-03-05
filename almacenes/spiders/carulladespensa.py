import scrapy


class CarulladespensaSpider(scrapy.Spider):
    name = "carulladespensa"
    allowed_domains = ["www.carulla.com"]
    start_urls = ["https://www.carulla.com/despensa"]

    def parse(self, response):
        pass
