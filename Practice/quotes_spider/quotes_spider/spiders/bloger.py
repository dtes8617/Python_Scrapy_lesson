# -*- coding: utf-8 -*-
import scrapy


class BlogerSpider(scrapy.Spider):
    name = 'bloger'
    allowed_domains = ['dtes8617.github.io']
    start_urls = ['http://dtes8617.github.io/']

    def parse(self, response):
        pass