# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,re,pymysql,pymongo
from scrapy.exporters import JsonItemExporter
from scrapy.conf import settings
import logging



class BaikespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DataSubmitTxtFile(object):
    def __init__(self):
        pass

    def process_item(self,item,spider):

        # 该id号为唯一的，作为关联HTMLPage和information的标志
        id = int(re.split('/',item['link'])[-1].split('>')[0])

        links = dict(
            {
                "id": id,
                "title": item['original_page_title'],
                "page_link" :item['link'],
                "relations": item['relation'],
            }
        )

        with open("data/relation_links.json",'a+',encoding='utf-8') as f:
            f.write(json.dumps(links,ensure_ascii=False) + '\n')

        with open("data/HtmlPage/" + item['original_page_title'] + str(id) + ".html",'w',encoding='utf-8') as f:
            f.write(item['original_page'])

        # 把每一个人的信息加一个id号
        item['information']['id'] = id

        with open("data/person_info.json",'a+',encoding='utf-8') as f:
            f.write(json.dumps(item['information'],ensure_ascii=False) + '\n')

        return item

class SubmitToMysql(object):
    """
    doc: for databasepipline
    """
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,user='baikespider',passwd='baikeSpider123.',db='baikeSpider',charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self,item, spider):
        # 该id号为唯一的，作为关联HTMLPage和information的标志
        id = int(re.split('/', item['link'])[-1].split('>')[0])

        links = dict(
            {
                "title": item['original_page_title'],
                "page_link": item['link'],
            }
        )

        logging.warning("success connect to mysql database", level = "INFO")
        sql = 'insert into baiduSpider(id,original_page) value (%s,%s)'
        try:
            self.cursor.execute(sql,(id,item['original_page']))
            self.conn.commit()
        except pymysql.Error as e:
            logging.warning(e,level="ERROR")

        return item

class SubmitToMongoDB(object):
    """
    doc:connect to mongoDB
    """
    def __init__(self):
        conn = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['PORT'],
        )
        self.db = conn[settings['MONGODB_DB']]
        self.page_collection = self.db['originalpage']
        self.info_collection = self.db['information']

    def process_item(self,item,spider):

        # 该id号为唯一的，作为关联HTMLPage和information的标志
        id = int(re.split('/', item['link'])[-1].split('>')[0])

        links = dict(
            {
                "title": item['original_page_title'],
                "page_link": item['link'],
            }
        )

        page = dict(
            {
                "page_id": id,
                "page_title": item['original_page_title'],
                "page_data": item['original_page'],
            }
        )

        info = dict(
            {
                "id":id,
                "links":links,
                "information":item['information'],
            }
        )
        try:
            self.page_collection.insert(page)
            logging.warning("web page added to page_collection",level="INFO",spider=spider)
            self.info_collection.insert(info)
            logging.warning("people info added to info_collection", level="INFO",spider=spider)
        except Exception as e:
            logging.warning(e,level="ERROR",spider=spider)

        return item


