# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArizonastateunivprojectItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    nameurl = scrapy.Field()
    sport = scrapy.Field()
    category = scrapy.Field()
    pass
