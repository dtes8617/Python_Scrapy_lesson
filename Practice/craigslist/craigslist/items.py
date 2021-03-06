# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CraigslistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    compensation = scrapy.Field()
    employment_type = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
