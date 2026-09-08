import scrapy
from ..items import TigerItem
from urllib.parse import urljoin
from scrapy import  Selector


class FtigerspiderSpider(scrapy.Spider):
    name = "ftigerspider"

    async def start(self):
        url = "https://flyingtiger.com/collections/shop-all?page=1"

        yield scrapy.Request(
            url=url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "wait_until": "domcontentloaded",
                    "timeout": 60000,
                },
            },
            callback=self.parse,
            cb_kwargs={"page_number": 1},
        )

    async def parse(self, response, page_number):
        page = response.meta["playwright_page"]

        try:
            await page.locator(
                "blooomreach-container h4.card__heading.h5 a"
            ).first.wait_for(timeout=60000)

            html = await page.content()
            selector = Selector(text=html)

            container = selector.css("blooomreach-container")

            product_urls = container.css(
                "h4.card__heading.h5 a::attr(href)"
            ).getall()

            for product_url in product_urls:
                product_url = urljoin(response.url, product_url)
                yield scrapy.Request(
                    product_url,
                    callback=self.parse_product,
                    meta={
                        "playwright": True,
                        "playwright_page_goto_kwargs": {
                            "wait_until": "domcontentloaded",
                            "timeout": 60000,
                        },
                    },
                )

            if page_number == 1:
                next_page = 2
                next_url = (
                    "https://flyingtiger.com/collections/shop-all"
                    f"?page={next_page}"
                )
                yield scrapy.Request(
                    next_url,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_goto_kwargs": {
                            "wait_until": "domcontentloaded",
                            "timeout": 60000,
                        },
                    },
                    callback=self.parse,
                    cb_kwargs={"page_number": next_page},
                )

        finally:
            await page.close()

    def parse_product(self, response):

        tiger_item = TigerItem()

        name = response.css(
            "div.product__title h1.title::text"
        ).get()

        price = response.css(
            "span.subtitle--s.price-item.price-item--regular::text"
        ).get()

        price = price.strip() if price else "No price"

        product_code_detail = response.css(
            "div.product__sku::text"
        ).get()

        product_code = (
            product_code_detail.split(":")[-1].strip()
            if product_code_detail
            else "No product code"
        )

        image_url = response.css(
            "div.product__media.media.media--transparent.gradient.global-media-settings "
            "img::attr(src)"
        ).get()

        image_url = (
            urljoin(response.url, image_url)
            if image_url
            else "No image link"
        )

        product_url = response.url

        tiger_item["name"] = name
        tiger_item["price"] = price
        tiger_item["product_code"] = product_code
        tiger_item["image_url"] = image_url
        tiger_item["product_url"] = product_url

        yield tiger_item
