# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,re
from scrapy.exporters import JsonItemExporter


class BaikespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DataSubmitTxtFile(object):
    def __init__(self):
        pass

    def process_item(self,item,spider):

        # links = dict(
        #     {
        #         "id": int(re.split('/',item['link'])[-1].split('>')[0]),
        #         "title": item['original_page_title'],
        #         "page_link" :item['link'],
        #     }
        # )
        # with open("data/relation_links.json",'a+',encoding='utf-8') as f:
        #     f.write(json.dumps(links) + '\n')
        #
        # with open("data/HtmlPage/" + item['original_page_title'] + ".html",'w',encoding='utf-8') as f:
        #     f.write(item['original_page'])

        with open("data/person_info.json",'a+',encoding='utf-8') as f:
            f.write(json.dumps(item['information']) + '\n')

        return item
