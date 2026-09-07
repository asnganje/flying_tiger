import scrapy
from ..items import TigerItem
from urllib.parse import urljoin

class FtigerspiderSpider(scrapy.Spider):
    name = "ftigerspider"

    async  def start(self):
        url = ("https://flyingtiger.com/collections/shop-all")
        yield scrapy.Request(
            url=url,
            meta={"playwright": True}
        )

    async def parse(self, response):
        products = response.css("h4.card__heading.h5 a::attr(href)").getall()

        for product_url in products:
            product_url = urljoin(response.url, product_url)
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True})

    def parse_product(self, response):
        tiger_item = TigerItem()
        name = response.css("div.product__title h1.title::text").get()
        price = response.css("span.subtitle--s.price-item.price-item--regular::text").get()
        price = price.strip() if price else "No price"
        product_code_detail = response.css("div.product__sku::text").get()
        product_code = product_code_detail.split(":")[-1].strip()
        image_url = response.css("div.product__media.media.media--transparent.gradient.global-media-settings img::attr(src)").get()
        image_url = urljoin(response.url, image_url) if image_url else "No image link"
        product_url = response.url
        tiger_item['name'] = name
        tiger_item['price'] = price
        tiger_item['product_code'] = product_code
        tiger_item['image_url'] = image_url
        tiger_item['product_url'] = product_url
        yield tiger_item


