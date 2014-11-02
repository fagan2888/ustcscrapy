# coding:utf-8

import	scrapy
from scrapy.http import Request
from bbs.items import BBSItem
import re

class BBSSpider(scrapy.Spider):
	name = 'bbs'
	allowed_domains	=	["bbs.ustc.edu.cn"]
	start_urls = ['http://bbs.ustc.edu.cn/cgi/bbsindex']
	
	def	parse(self,	res):
		
		urls = res.xpath('//a/@href').extract()
		for url in urls:
			if re.match('bbstcon\?board=.+&file=.+', url):
				yield Request('http://bbs.ustc.edu.cn/cgi/'+url, callback=self.parse_item)
				
			else: 
				yield Request('http://bbs.ustc.edu.cn/cgi/'+url, callback=self.parse)
			
	
	def parse_item(self, res):
		item = BBSItem()
		item['url'] = res.url
		item['title'] = res.xpath('/html/head/title/text()').extract()
		item['content'] = res.xpath('//div[@class="post_text"]/text()').extract()
		yield item
		