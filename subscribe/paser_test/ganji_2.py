#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import os,datetime,string
import chardet
import sys
import re
import time
from bs4 import BeautifulSoup
import hashlib
#md5=hashlib.md5(‘字符串’.encode(‘utf-8′)).hexdigest()
#print(md5)

import hashlib
#a = {'a':'aaa','b':'bbb'}

#a['c']='ccc'
#>>> a
#{'a': 'aaa', 'c': 'ccc', 'b': 'bbb'}
#>>> a.has_key('a')
#True
#>>> a.has_key('d')
#False
#>>> a = {}
#>>> a
#{}
#>>> a['a']='aaa'
#>>> a
#{'a': 'aaa'}
class Info(object):
	def __init__(self,title=' ',href = ' ',addr = ' ',description=' ',shijian = 3600*60,price = 0,pic = '无'):
		self.title = title
		self.href = href
		self.addr = addr
		#self.time_str = ''
		self.description=description
		self.shijian = shijian
		self.price = price
		self.pic = pic

	def __str__(self):
		res =  'title'+self.title+'\n'
		res = res + 'href'+self.href+'\n'
		res = res + 'addr'+self.addr+'\n'
		res = res + 'description'+self.description
		return res
	def get_addr(self):
		return self.addr
	#__repr__=__str__



##赶集网搜索的结果在首页上并没有给出详细的时间，只是‘一小时以内’之类的，并且有些时间，即使在详细页面上也没有
##真心搞不懂他们是怎么搞的，所以这里的策略是，对标题的链接进行hash，放入一个容器，定时重新刷新容器，防止容器过大	
##所以这里有个想法，就是只要用户提供正确的网址，程序自动匹配正确的爬虫进行分析
class tc58(object):
	def __init__(self,url):
		self.__url = url
		self.__addr_infos = []
		self.__first = True
		self.__last_time = 0.0
		self.__loop_time = 5.0
		self.__map = {}
		self.__base_url = ''
	def load_page(self):
		opener = urllib2.build_opener()
		f = opener.open(self.__url)
		html = f.read()
		self.__html = html
		f.close()
##		html_file = open('ganji.txt','w')
##		html_file.write(html)
##		html_file.close()
##		time.sleep(20)
		return html
	
	def load_page1(self):
		html_file = open('ganji.txt','r')
		html =html_file.read()
		html_file.close()
		self.__html = html
		#print html
		#time.sleep(20)
		return html
	

	def get_res(self):
		##返回的结果
		res = []
		#self.__addr_infos = []
		soup = BeautifulSoup(self.__html)
		lis = soup.find_all('li',class_='list-img clearfix')
		#print len(lis)
		for li in lis:
			info = Info()
			titles_all = li.find_all('div',class_='info-title')
			#print len(titles_all)
			if(titles_all is not None and len(titles_all)>0):
				title_all = titles_all[0]
				title =  title_all.a.get_text().strip()
				#print title
				href =  title_all.a['href'].strip()
				#print href
				info.title = title
				info.href = self.__base_url + href
			info.description = li.get_text().strip()
			#print info.description

			##下面开始计算新的信息
			href_md5 = hashlib.md5(info.href.encode('utf-8')).hexdigest()
			if not self.__map.has_key(href_md5):
				res.append(info)
				self.__map[href_md5] = info

		print 'res len:'
		print len(res)
		return res

	def send_mail(self):
		pass
	def get_addr_infos(self):
		return self.__addr_infos
	def run(self):
		self.load_page()
		return self.get_res()

	def resize_map(self):
		seed = random.randint(1,30)
		i = 0
		for key in self.__map.keys():
			if not i%seed:
				del self.__map[key]
			i = i+1



	def fun_loop(self):
		num = 0
		##初始化填充map
		self.run()
		
		for i in range(100000):
			res = self.run()
			if len(self.__map)>1000:
				resize_map()
				#self.run()
				continue
			if(len(res)>0):
				print 'hello we recv a new recore!!'
				print '**'*20
				for i in res:
					print i.href
			time.sleep(5)
			
#租房
if __name__ == '__main__':
	tc = tc58('http://sz.ganji.com/fang1/_%E8%85%BE%E8%AE%AF/')
	tc.fun_loop()


#s = u'11月2日'

#s.encode('utf-8')
#print s[0]
#print s[1]
#print s[2]
#print s[3]
#print s[4] == u'日'

