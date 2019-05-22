# -*- coding: utf-8 -*-
from time import sleep
import pymysql
import glob
import os
import csv
from bbc_learning_course.items import BbcLearningCourseItem
from scrapy.loader import ItemLoader
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
        l = ItemLoader(BbcLearningCourseItem(), response = response)
        title = response.xpath('//div[@class="widget widget-bbcle-activitytitle"]/h3/text()').extract_first()
        url = response.request.url

        l.add_value('title',title)
        l.add_value('url',url)

        yield l.load_item()

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key = os.path.getctime)
        mydb = pymysql.connect(host = 'localhost', user = 'root', password = '123456', db = 'lesson')
        cursor = mydb.cursor()
        self.logger.info('cursor constructed.')
        csv_data = csv.reader(open(csv_file))
        self.logger.info('{}'.format(next(csv_data)))
        # csv_data = csv.reader(open(csv_file, 'r'))
        self.logger.info('opened file')
        

        row_count = 0
        for row in csv_data:
            self.log('the data is {}'.format(row))

            if row_count != 0:
                cursor.execute('INSERT IGNORE INTO lesson.bbc_learning_course(Title, URL) VALUES(%s, %s)',row)
                self.logger.info('import {}th row'.format(row_count))
            row_count+=1
        mydb.commit()
        cursor.close()