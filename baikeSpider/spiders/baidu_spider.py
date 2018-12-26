import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule
from baikeSpider.items import BaikespiderItem
from collections import OrderedDict
import re

class baiduSpider(CrawlSpider):
    name = "baiduSpider"

    allowed_domain = ["baike.baidu.com"]
    start_urls = ["https://baike.baidu.com/item/李幼斌/12503",
                  ]

    # response中提取链接的匹配规则，得到符合条件的链接
    # pattern = '//div[@id="slider_relations"]/ul/li/a'
    pattern = '/item/*.'
    pagelink = LinkExtractor(allow=pattern,restrict_xpaths='//div[@id="slider_relations"]/ul/li/a')

    # 定义爬取的规则
    rules = (
        Rule(pagelink, callback='parse_items', follow = True),
    )

    def parse_items(self, response):
        item = BaikespiderItem()
        # response.selector.register_namespace('d', 'https://baike.baidu.com')
        item['link'] = str(response)

        item['relation'] = [''.join(('https://baike.baidu.com',i)) for i in response.xpath('//div[@id="slider_relations"]/ul/li//a/@href').extract()]

        item['original_page'] = response.text
        item['original_page_title'] = response.xpath('head/title/text()').extract()[0]

        # 提取个人信息
        property_name = response.xpath('//dt[@class="basicInfo-item name"]/text()')
        # xpath 选择所有兄弟节点 /following-sibling::*，选择兄弟节点的第一个following-sibling::*[1]
        property_value = response.xpath('//dd[@class="basicInfo-item value"]/text()')

        # split方法中不带参数时，表示分割所有换行符、制表符、空格
        property_name = [''.join(i.extract().split()) for i in property_name]
        property_value = [''.join(re.split('[《》、]', i.extract())) for i in property_value if i]

        information = OrderedDict({})
        for k, v in zip(property_name, property_value):
            information[k] = v.strip('\n')
        item['information'] = information

        yield item


    # TODO 这是一个获取页面链接的例子
    # def __init__(self, *args, **kwargs):
    #     super(baiduSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ['https://baike.baidu.com/item/李幼斌/12503']
    #
    # def parse(self, response):
    #     link = LinkExtractor(restrict_xpaths='//div[@id="slider_relations"]/ul/li/a')
    #     links = link.extract_links(response)
    #     if links:
    #         for link_one in links:
    #             print("relation_url:" + link_one.url + "\n" + "relation_name:" + link_one.text.strip())


    # TODO 这个是scrapy的另一个内置Spider，通过调用具体的spider
    # def start_requests(self):
    #     start_urls = ["https://baike.baidu.com/item/李幼斌/12504",
    #                   ]
    #     for url in start_urls:
    #         # 包含yield语句的函数是一个生成器
    #         # 生成器每次产生一个值（yield语句），函数被冻结，被唤醒后再产生一个值，生成器是一个不断产生值的函数
    #         yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
    #
    # def parse(self, response):
    #     pass
