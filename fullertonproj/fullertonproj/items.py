# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FullertonprojItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    sport = scrapy.Field()
    position = scrapy.Field()
    url = scrapy.Field()
    pass
