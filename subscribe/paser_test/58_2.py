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
	def __init__(self,title=' ',href = ' ',addr = ' ',description=' ',shijian = 3600*60,price = 1000000,pic = '无'):
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
	def get_58_time(self,all):
                #取得中文，也就是后面的单位
		r = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\\n\\r]", "", all)
                #取得前面的数字
		num = filter(str.isdigit, all)
		num = num.decode('utf-8')
		r = r.decode('utf-8')
		print u'单位：'+r.strip()
		print u'值：' + num
		r = r.strip()
		print type(r)
		num = num.strip()
		num = int(num)
		if num == 36:
			print 'trueuuu'
		if r == u'分钟'.encode('utf-8') or r == u'分钟 '.encode('utf-8'):
			#print '这里是分钟'
			return num
		if r == u'小时'.encode('utf-8') or r == u'小时 '.encode('utf-8'):
			return num*60
		else:
			return 3600*60

	def parse_58(self):
		self.__addr_infos = []
		soup = BeautifulSoup(self.__html)
		tables = soup.find_all('table',class_="tblist tb-jjgr")
		import sys
		#sys.setrecursionlimit(1000000) #例如这里设置为一百万
		print len(tables)
		table = None
		if(len(tables)>0):
			table = tables[0]
		trs = table.find_all('tr')
		patt = re.compile(r"\((.*?)\)", re.I|re.X)
		for tr in trs:
			info = Info()
			t2s = tr.find_all('td',class_='t')
			if len(t2s)>0:
				t2 = t2s[0]
				#print t2.a.string
				#info.title = t2.a.string
				info.href =  t2.a['href']
				#contents = t2.contents
				#print contents
				#全部信息
				#可以进行三部分解析
				#第一部分是标题，第二部分是正文，包含时间信息，第三部分是地址
				#所以关键是解析这一段的时间
				con = str(t2.get_text().encode('utf-8'))
				info.description = con
				print con
				print type(con)

				all = patt.findall(con)

				t = all[len(all)-1]
				time_str = t
				time_num = self.get_58_time(time_str)

				print 'info:'
				print 'title:'+info.title
				print 'href:'+info.href
				print 'price:%s'%info.price
				print 'shijia:%d'%info.shijian
				self.__addr_infos.append(info)
				time.sleep(5)

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
		##第一个的时间一定是最小的
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
		self.__last_time = min_time
		return res

	def fun_loop(self):
		##指定第一次，来初始化last
		for i in range(100000):
			self.run()
			#all =  self.get_addr_infos()
			if len(self.__addr_infos) == 0:
				continue
			if self.__first == True:

				if(len(self.__addr_infos)>0):
					self.__last_time = self.__addr_infos[0].shijian
					print 'hah:%d'%self.__last_time
					#for i in self.__addr_infos:
					#	print i.shijian
				self.__first = False
				print 'last_time:%d'%int(self.__last_time)

			else:
				new = self.find_head()
				print 'len(new):%d'%len(new)
				print 'last_time:%d' % int(self.__last_time)
			time.sleep(self.__loop_time)

	#print len(all)

if __name__ == '__main__':
	tc = tc58('http://wh.58.com/jiajiaogeren/?key=%E8%8B%B1%E8%AF%AD')
	tc.fun_loop()


#s = u'11月2日'

#s.encode('utf-8')
#print s[0]
#print s[1]
#print s[2]
#print s[3]
#print s[4] == u'日'

