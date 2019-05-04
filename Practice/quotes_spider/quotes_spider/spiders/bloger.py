# -*- coding: utf-8 -*-
import scrapy


class BlogerSpider(scrapy.Spider):
    name = 'bloger'
    allowed_domains = ['dtes8617.github.io']
    start_urls = ['http://dtes8617.github.io/']

    def parse(self, response):
        articles =  response.xpath('//*[@class="post-block"]')
        
        
        for article in articles:
            title = article.xpath('.//a[@class="post-title-link"]/text()').extract_first()
            tags = article.xpath('.//span[@itemprop="name"]/text()').extract_first()
            abstract = ''.join(article.xpath('.//div[@class="post-body"]/p/text()').extract())

            print('\n')
            print(title)
            print(tags)
            print(abstract)
            print('\n')