# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikespiderItem(scrapy.Item):
    # define the fields for your item here like:
    original_page = scrapy.Field()
    original_page_title = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    information = scrapy.Field()
    relation = scrapy.Field()
