# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HtmlPipeline(object):
    # def open_spider(self, spider):
    #     self.file = open('items.jl', 'wb')
    #
    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        # some item data middle-processing here
        return item
