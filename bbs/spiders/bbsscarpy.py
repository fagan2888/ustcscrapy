# coding:utf-8

import	scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bbs.items import BBSItem
import re

class BBSSpider(CrawlSpider):
	name = 'bbs'
	allowed_domains	=	["bbs.ustc.edu.cn"]
	start_urls = ['http://bbs.ustc.edu.cn/cgi/bbsindex']
	rules = [
		Rule(LinkExtractor(allow=('bbscon\?bn=.+&fn=.+' )), callback='parse_item', follow=False),
		Rule(LinkExtractor(allow=('bbsdoc\?board=[^&]+', 'bbsdoc\?board=[^&]+&start=\d+'))),
		Rule(LinkExtractor(deny=('.+')))
	]
	
	def	parse_start_url(self, res):
		try:
			urls = LinkExtractor(allow=('bbsdoc\?board=[^&]+', 'bbsdoc\?board=[^&]+&start=\d+')).extract_links(response)
			for url in urls:
				print url.text
				yield Request(url.url, callback='parse')
		except:
			pass
	
	def parse_item(self, res):
		item = BBSItem()
		item['url'] = res.url
		item['title'] = res.xpath('/html/head/title/text()').extract()
		item['content'] = res.xpath('//div[@class="post_text"]/text()').extract()
		yield item
		