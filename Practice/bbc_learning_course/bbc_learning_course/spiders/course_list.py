# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException


class CourseListSpider(Spider):
    name = 'course_list'
    allowed_domains = ['bbc.co.uk/learningenglish/english/']

    def start_requests(self):
        self.driver = webdriver.Chrome('E:/Users/Jude/Documents/GitHub/Python_Scrapy_lesson/chromedriver')
        self.driver.get('http://www.bbc.co.uk/learningenglish/english/')
        sel = Selector(text = self.driver.page_source)
        level_list = sel.xpath('//div[@id="navIndex-0"]//a/@href').extract()

        for level in level_list:
            sleep(3)
            self.driver.get('http://www.bbc.co.uk' + level)
            sel = Selector(text = self.driver.page_source)
            try:
                lesson = sel.xpath('//div[@class="details"]/h3/a/@href').extract()
                for link in lesson: 
                    url = 'http://www.bbc.co.uk' + link
                    yield Request(url, callback = self.parse_lesson)
            except NoSuchElementException:
                continue

        self.logger.info('All tasks done!')
        self.driver.quit()

    def parse_lesson(self, response):
        title = response.xpath('//div[@class="widget widget-bbcle-activitytitle"]/h3/text()').extract_first()
        url = response.request.url
        yield {'Title': title, 'URL': url}
