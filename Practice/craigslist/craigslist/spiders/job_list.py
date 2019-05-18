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

        next_page_url = response.xpath('//a[@title="next page"]/@href').extract_first()        
        yield Request(response.urljoin(next_page_url))
        # for url in urls:
        #     yield Request(url, callback = self.parse_details)

    def parse_details(self, response):
        l = ItemLoader(CraigslistItem(), response = response)
        date = response.xpath('//time[@class="date timeago"]/@datetime').extract_first()[:10]
        title = response.xpath('//span[@id="titletextonly"]/text()').extract_first()
        url = response.request.url
        compensation = response.xpath('//span[text()="compensation: "]/b/text()').extract_first()
        employment_type = response.xpath('//span[text()="employment type: "]/b/text()').extract_first()
        image_urls = response.xpath('//div[@id="thumbs"]//a/@href').extract()

        l.add_value('date', date)
        l.add_value('title', title)
        l.add_value('url', url)
        l.add_value('compensation', compensation)
        l.add_value('employment_type', employment_type)
        l.add_value('image_urls', image_urls)

        yield l.load_item()
        # yield {'date': date, 'title':title}