# -*- coding: utf-8 -*-
import scrapy
import os
from urlparse import urlparse

from doubangroup.items import TopicItem


class GroupSpider(scrapy.Spider):
    '''
    usage:
        scrapy crawl group -a group_id=467799 -a date_prefix=04-26
    see result:
        curl http://mycloud:6800/listjobs.json?project=doubangroup
    '''
    name = "group"
    allowed_domains = ["www.douban.com"]

    TOPIC_SIZE_PER_PAGE = 25
    DOUBAN_GROUP_URL_TEMPLATE = 'https://www.douban.com/group/%s/discussion?start=%s'

    def __init__(self, date_prefix, group_id, *args, **kwargs):
        super(GroupSpider, self).__init__(*args, **kwargs)
        self.curr = 0
        self.date_prefix = date_prefix
        self.group_id = group_id

    def gen_url(self):
        return self.DOUBAN_GROUP_URL_TEMPLATE % (self.group_id, self.curr)

    def start_requests(self):
        return [scrapy.FormRequest(self.gen_url())]

    def parse(self, response):
        contain_present_topic = False
        for tr in response.xpath("//table[@class='olt']//tr[@class='']"):
            pub_time = tr.xpath('./td[4]/text()').extract()[0]
            if pub_time.startswith(self.date_prefix):
                contain_present_topic = True
            else:
                continue                
            title_node = tr.xpath('./td[1]/a')
            author_node = tr.xpath('./td[2]/a')
            title = title_node.xpath('./@title').extract()[0]
            topic_link = title_node.xpath('./@href').extract()[0]
            topic_id = get_link_last_dir(topic_link)
            author_name = author_node.xpath('./text()').extract()[0]
            author_link = author_node.xpath('./@href').extract()[0]
            author_id = get_link_last_dir(author_link)

            item = TopicItem()
            item['topic_id'] = topic_id
            item['title'] = title
            item['author_id'] = author_id
            item['author_name'] = author_name
            item['link'] = topic_link
            item['pub_time'] = pub_time
            yield item

        self.curr += self.TOPIC_SIZE_PER_PAGE
        if contain_present_topic:
            yield scrapy.Request(self.gen_url(), callback=self.parse)


def get_link_last_dir(link):
    path = urlparse(link).path
    return os.path.basename(os.path.normpath(path))
