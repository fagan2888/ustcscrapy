# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import hashlib

class BBSPipeline(object):
	def process_item(self, item, spider):
		
		cur = self.conn.cursor()
		digest = hashlib.md5(item['url'].encode('utf-8')).hexdigest()[:10]
		if digest in self.visited:
			return
		
		self.visited.add(digest)
		data = (digest, item['url'], item['title'][0].encode('utf-8'), ''.join(item['content']).encode('utf-8') )
		# print data
		cur.execute("insert into post (url_hash, url, title, content) values(%s,%s,%s,%s) " ,  data)
		cur.close()
		#with open(hashlib.md5(item['title'][0].encode('utf-8')).hexdigest() + '.txt', 'wb') as f:
		#	f.write(''.join(item['content']).encode('utf-8'))
		
		self.batch = self.batch + 1
		if self.batch >=100:
			self.conn.commit()
			self.batch = 0
			
		#return item

	def open_spider(self, spider):
		self.batch = 0
		self.visited =  set()
		self.conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='bbs',port=3306,charset = 'utf8')
		
	def close_spider(self, spider):
		self.conn.commit()
		self.conn.close()