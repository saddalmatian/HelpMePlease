# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HackernewItem(scrapy.Item):

    rank = scrapy.Field()
    title = scrapy.Field()
    id_post = scrapy.Field()
    link = scrapy.Field()
    point = scrapy.Field()
    user = scrapy.Field()
    time_post = scrapy.Field()
    comment = scrapy.Field()

    pass
