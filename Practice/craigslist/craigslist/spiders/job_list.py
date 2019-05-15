# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from craigslist.items import CraigslistItem


class JobListSpider(scrapy.Spider):
    name = 'job_list'
    allowed_domains = ['newyork.craigslist.org/search/egr']
    start_urls = ['http://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        l = ItemLoader(CraigslistItem(), response = response)

        date = response.xpath('//time[@class="result-date"]/@datetime').extract()
        title =  response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        urls = response.xpath('//a[@class="result-title hdrlnk"]/@href').extract()

        for d, t, u in zip(date, title, urls): 
            l.add_value('date', d)
            l.add_value('title', t)
            l.add_value('urls', u)
            break

        yield l.load_item()
        # for url in urls:
        #     yield Request(url, callback = self.parse_details)

    def parse_details(self, response):
        pass