# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    '''used to debug http header'''
    name = "test"
    allowed_domains = ["localhost"]
    start_urls = (
        'http://localhost:9999',
    )

    def parse(self, response):
        pass
