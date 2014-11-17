#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import os,datetime,string
import chardet
import sys
import re
import time
from bs4 import BeautifulSoup

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

class tc58(object):
	def __init__(self,url):
		self.__url = url
		self.__addr_infos = []
		self.__first = True
		self.__last_time = 0.0
		self.__loop_time = 5.0
	def load_page(self):
		opener = urllib2.build_opener()
		f = opener.open(self.__url)
		html = f.read()
		self.__html = html
		f.close()
		return html
	
	def load_page1(self):
		html_file = open('ganji.txt','r')
		html =html_file.read()
		html_file.close()
		self.__html = html
		print html
		#time.sleep(20)
		return html
	
	       
	def get_58_time(self,all):
		##这里对于某月某日的日期实际上是不处理的，因为那些时间至少是一天以前的，没哟必要处理
		##则可以返回一个很大的时间
		print 'in get_time'
		print type(all)
                #取得中文，也就是后面的单位
		r = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\\n\\r]", "", all)
                #取得前面的数字
		num = filter(str.isdigit, all)

		print '单位：'+r.strip()
		print '值：' + num
		##有些记录就没有时间这一项，比如以商家来代替时间
		##所以对于这种情况，直接返回最大的时间
		if len(num)==0:
			return 3600*60
		r = r.strip()
		print 'len (r):%d'%len(r)
		print 'len(u分钟):%d'%len(u'分钟'.encode('utf-8'))
		num = num.strip()
		num = int(num)

		if r == u'分钟'.encode('UTF-8') or r == u'分钟 '.encode('utf-8'):
			print '这里是分钟'
			return num
		elif r == u'小时'.encode('utf-8') or r == u'小时 '.encode('utf-8'):
			print '这里是小时'
			return num*60
		else:
			print '什么都没有匹配到'
			return 3600*60

	def parse_58(self):
		self.__addr_infos = []
		soup = BeautifulSoup(self.__html)
		tables = soup.find_all('div',class_="layoutlist")
		print len(tables)
		
		table = None
		if(len(tables)>0):
			table = tables[0]
		trs = table.find_all('dl')
		patt = re.compile(r"\((.*?)\)", re.I|re.X)
		for tr in trs:
			info = Info()
			t2s = tr.find_all('dd',class_='feature')
			if len(t2s)>0:
				t2 = t2s[0]
				li = t2.find_all('li',class_="js-item")
				print 'len(li):%d'%len(li)
				if(li is not None and len(li) is not 0):
					li = li[0]
				
				#print t2.a.string
				info.title = li.a.get_text().strip()
				info.href =  t2.a['href']

				tu = li.find_all('span',class_='i-tu');
				if(tu is not None and len(tu)>0):
					info.pic = tu[0].get_text().strip()

				info.description = t2.p.get_text().strip()

				i = t2.find_all('i',class_="mr8")
				if i is not None:
					time_str = i[0].get_text().strip()
					print "*"*30
					print 'time_str'
					print time_str
					
					info.shijian = self.get_58_time(time_str.encode('UTF-8'))

				print 'info:'
				print 'title:'+info.title
				print 'href:'+info.href
				print 'price:%s'%info.price
				print 'shijia:%d'%info.shijian
				self.__addr_infos.append(info)
				#time.sleep(1)

	def send_mail(self):
		pass
	def get_addr_infos(self):
		return self.__addr_infos
	def run(self):
		self.load_page()
		self.parse_58()


	def find_head(self):
		##得到实际的上次的时间
		self.__last_time = float(self.__last_time) + float(self.__loop_time/60.0)
		min_time = 0.0
		##返回的结果
		res = []
		all = self.__addr_infos
		##假设第一个的时间一定是最小的
		
		if len(all)>0:
			min_time = all[0].shijian
		for item in all:
			##单位是s
			shijian = item.shijian
			#print '时间:%s'%shijian
			if (shijian+1) < self.__last_time:
				print "**"*15
				print item.shijian
				res.append(item)
				print "**"*15
			#if shijian<min_time:
                         #       min_time = shijian

		self.__last_time = min_time
		return res

	def fun_loop(self):
		num = 0
		##指定第一次，来初始化last
		for i in range(100000):
			self.run()
			#all =  self.get_addr_infos()
			if len(self.__addr_infos) == 0:
				continue
			if self.__first == True:
				
				if(len(self.__addr_infos)>0):
					self.__last_time = self.__addr_infos[0].shijian
					#print 'hah:%d'%self.__last_time
					#for i in self.__addr_infos:
					#	print i.shijian
				self.__first = False
				print 'last_time:%d'%int(self.__last_time)
		
			else:
				new = self.find_head()
				print 'len(new):%d'%len(new)
				num = num + len(new)
				print num
				print 'last_time:%d' % int(self.__last_time)
			time.sleep(self.__loop_time)
	
	#print len(all)
if __name__ == '__main__':
	tc = tc58('http://wh.ganji.com/ipadpingban/?original=ipad')
	tc.fun_loop()


#s = u'11月2日'

#s.encode('utf-8')
#print s[0]
#print s[1]
#print s[2]
#print s[3]
#print s[4] == u'日'

