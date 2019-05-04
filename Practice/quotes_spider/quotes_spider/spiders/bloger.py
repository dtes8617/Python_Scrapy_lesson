# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader

from quotes_spider.items import QuotesSpiderItem


class BlogerSpider(Spider):
    name = 'bloger'
    allowed_domains = ['dtes8617.github.io']
    start_urls = ['http://dtes8617.github.io/']

    def parse(self, response):
        l = ItemLoader(item=QuotesSpiderItem(), response=response)

        articles =  response.xpath('//*[@class="post-block"]')
        
        for article in articles:
            
            tags = article.xpath('.//span[@itemprop="name"]/text()').extract_first()
            abstract = ''.join(article.xpath('.//div[@class="post-body"]/p/text()').extract())
            title = article.xpath('.//a[@class="post-title-link"]/text()').extract_first()

            
            l.add_value('tags', tags)
            l.add_value('abstract', abstract)
            l.add_value('title', title)

        return l.load_item()