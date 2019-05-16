# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from craigslist.items import CraigslistItem


class JobListSpider(scrapy.Spider):
    name = 'job_list'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['http://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        urls = response.xpath('//a[@class="result-title hdrlnk"]/@href').extract()

        for url in urls: 
            yield Request(url, callback = self.parse_details) 
        # for url in urls:
        #     yield Request(url, callback = self.parse_details)

    def parse_details(self, response):
        l = ItemLoader(CraigslistItem(), response = response)
        date = response.xpath('//time[@class="date timeago"]/@datetime').extract_first()[:10]
        title = response.xpath('//span[@id="titletextonly"]/text()').extract_first()
        url = response.request.url
        l.add_value('date', date)
        l.add_value('title', title)
        l.add_value('url', url)
        
        yield l.load_item()
        # yield {'date': date, 'title':title}