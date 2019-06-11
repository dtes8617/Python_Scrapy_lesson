# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from selenium import webdriver
from scrapy.selector import Selector
from time import sleep

class CatchLessonSpider(scrapy.Spider):
    name = 'catch_lesson'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/subjects/']

    def parse(self, response):
        topics = response.xpath('//li[@class="margin-bottom-large padding-right-medium"]//span[@class="head-3 large-up-head-2 text--bold block"]/text()').extract()
        linkages = response.xpath('//a[@class="text--blue"]/@href').extract()

        for topic, link in zip(topics, linkages):
            link = response.urljoin(link)
            yield Request(link, meta = {'topic': topic}, callback = self.parse_lesson)

    def parse_lesson(self, response):
        driver = webdriver.Chrome('/Users/jude/Documents/GitHub/Python_Scrapy_lesson/chromedriver_mac')
        driver.get(response.request.url)

        try: 
            while driver.find_element_by_xpath('//div[@class="text-center"]/button'):
                driver.find_element_by_xpath('//div[@class="text-center"]/button').click()
                sleep(2)
        except:
            page_source = driver.page_source
            sel = Selector(text = page_source)

        courses_info = sel.xpath('//tr[@itemtype="http://schema.org/Event"]')
        topic = response.meta['topic']

        for course in courses_info:
            institute = course.xpath('.//a[@class="uni-name text--charcoal hover-text--underline"]/text()').extract_first()
            course_name = course.xpath('.//span[@class="course-name-text text--bold"]/text()').extract_first()
            platform = course.xpath('.//a[@class="initiativelinks text--charcoal text--italic hover-text--underline"]/text()').extract_first()
            full_star = course.xpath('.//i[@class="icon-star icon--xxsmall"]').extract()
            semi_star = course.xpath('.//i[@class="icon-star-half icon--xxsmall"]').extract()
            star = len(full_star) + 0.5*len(semi_star)
            yield {
            'topic':topic, 
            'institute': institute,
            'course_name': course_name,
            'platform': platform,
            'star': star
            }
