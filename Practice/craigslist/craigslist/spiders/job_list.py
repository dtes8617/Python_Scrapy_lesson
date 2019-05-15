# -*- coding: utf-8 -*-
import scrapy


class JobListSpider(scrapy.Spider):
    name = 'job_list'
    allowed_domains = ['newyork.craigslist.org/search/egr']
    start_urls = ['http://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        pass
