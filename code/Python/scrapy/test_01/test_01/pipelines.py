# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from turtle import title
import openpyxl


class DoubanPipeline(object):

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active()
        self.ws.title = 'TOP250'
        self.ws.append(('标题', '评分', '主题'))

    def close_spider(self, spider):
        self.wb.save('movieData.xlsx')

    def process_item(self, item, spider):
        title = item.get('title', '')
        rank = item.get('rank', '')
        subject = item.get('subject', '')
        self.ws.append((title, rank, subject))
        return item
