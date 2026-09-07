# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

import scrapy

class TigerItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    product_details = scrapy.Field()
    image_url = scrapy.Field()
    product_coode = scrapy.Field()

