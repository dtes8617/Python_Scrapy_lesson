# -*- coding: utf-8 -*-
import scrapy


class FacebookSpider(scrapy.Spider):
    name = 'facebook'
    allowed_domains = ['www.facebook.com/tstartel/?epa=SEARCH_BOX']
    start_urls = ['http://www.facebook.com/tstartel/?epa=SEARCH_BOX/']

    def parse(self, response):
        context = response.xpath('//*[@class="text_exposed_root"]/p/text()').extract()
        yield {'Article': context}
