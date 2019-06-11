# -*- coding: utf-8 -*-
import scrapy


class CatchLessonSpider(scrapy.Spider):
    name = 'catch_lesson'
    allowed_domains = ['classcentral.com/subjects']
    start_urls = ['http://classcentral.com/subjects/']

    def parse(self, response):
        pass
