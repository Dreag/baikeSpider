# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter


class BaikespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DataSubmitJsonFile(object):

    def process_item(self, item, spider):
        with open("data/" + item['original_page_title'] + ".txt", 'wb' ) as f:
            f.write(bytes(item))
        return item