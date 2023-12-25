# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from test_01.items import MovieItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    # start_urls = ['https://movie.douban.com/top250']

    def start_requests(self):
        for page in range(10):
            yield Request(url=f'https://movie.douban.com/top250?start={page * 25}&filter=')

    def parse(self, response):
        sel = Selector(response)
        sel_list = sel.css('#content > div > div.article > ol > li')
        for sel_item in sel_list:
            movie_item = MovieItem()
            movie_item['title'] = sel_item.css('span.title::text').extract_first()
            movie_item['rank'] = sel_item.css('span.rating_num::text').extract_first()
            movie_item['subject'] = sel_item.css('span.inq::text').extract_first()
            yield movie_item

        # href_list = sel.css('div.paginator > a::attr(href)')
        # for href in href_list:
        #     url = response.urljoin(href.extract())
        #     print(url)
        #     yield Request(url=url)
