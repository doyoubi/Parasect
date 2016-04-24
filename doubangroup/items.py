# -*- coding: utf-8 -*-
import scrapy


class TopicItem(scrapy.Item):
    topic_id = scrapy.Field()
    title = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    link = scrapy.Field()
    pub_time = scrapy.Field()
