# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AndersonprojectItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    imgurl = scrapy.Field()
    category = scrapy.Field()
    sport = scrapy.Field()
    pass
