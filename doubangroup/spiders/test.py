# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["localhost"]
    start_urls = (
        'http://localhost:9999',
    )

    def parse(self, response):
        pass
