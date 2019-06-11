# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class CatchLessonSpider(scrapy.Spider):
    name = 'catch_lesson'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/subjects/']

    def start_request(self, response):
        topics = response.xpath('//li[@class="margin-bottom-large padding-right-medium"]//span[@class="head-3 large-up-head-2 text--bold block"]/text()').extract()
        linkages = response.xpath('//a[@class="text--blue"]/@href').extract()

        for topic, link in zip(topics, linkages):
            link = response.urljoin(link)
            return Request(link, meta = {'topic': topic}, callback = self.parse)

    def parse(self, response):
        self.logger.info('yes')
        topic = response.meta['topic']
        return {'topic':topic}
