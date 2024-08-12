# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WalmartproductItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    list_price = scrapy.Field()
    sell_price = scrapy.Field()
