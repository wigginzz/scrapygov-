# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import scrapy
import urlparse
from scrapy.contrib.loader import ItemLoader, Identity,MapCompose
from fun.items import MeizituItem


class Join(object):

    def __init__(self, separator=u' '):
        self.separator = separator

    def __call__(self, values):
        for i in range(len(values)):
        	values[i] = self.separator + values[i].encode('utf-8')
        #print(self.separator.join(values.encode("utf-8")))
        #return self.separator.join(values)
        return values
                                             

class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["gov.cn"]
    # 首页访问URL
    start_urls = (
        'http://sousuo.gov.cn/column/45044/2.htm',
    )
    
    def parse(self, response):
        sel = Selector(response)
        print(self.start_urls)
        for i in self.start_urls:
        	request = scrapy.Request(i, callback=self.parse_item)
        	yield request
        links = []
        i = 0
        for link in sel.xpath('//h4/a/@href').extract():
            links.append(link)
           
	linksLen = links.__len__()
	for i in range(0, links.__len__())[::-1]:
		link = links[i]
		print(link)
        	
        	request = scrapy.Request(link, callback=self.parse_item,priority=linksLen)
        	linksLen = linksLen-1
            	yield request
        
        # 获取之后访问URL
        pages = sel.xpath("//div[@class='newspage cl']/ul/li[1]/a/@href").extract()
        print("ssssssssssssssssssss")
        page_link = pages[0]
        print("ssssssssssssssssssss")
        if page_link.startswith('http://sousuo.gov.cn'):
            request = scrapy.Request(page_link, callback=self.parse)
            yield request

    # 解析URL获得下载图片URL
    def parse_item(self, response):
        # 解析http://www.meizitu.com/a/5336.html获取图片URL
        print(self)
        print(response)
        l = ItemLoader(item=MeizituItem(), response=response)
        l.add_xpath('image_urls', "//div[@class='pages_content']/p/img/@src",MapCompose(lambda i: urlparse.urljoin(response.url, i)))
	l.add_xpath('title',"//div[@class='article oneColumn pub_border']/h1/text()")
        
        l.add_xpath('image_content', "//div[@class='pages_content']/p/span/descendant-or-self::*/text()")
	l.add_xpath('content',"//div[@class='pages_content']/p/text()")
        l.add_value('url', response.url)
        return l.load_item()
