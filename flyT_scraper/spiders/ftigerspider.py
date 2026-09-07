import scrapy


class FtigerspiderSpider(scrapy.Spider):
    name = "ftigerspider"
    allowed_domains = ["flyingtiger.com"]
    start_urls = ["https://flyingtiger.com/collections/shop-all"]

    def parse(self, response):
        pass
