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
	def __init__(self,title='',href = '',addr = '',description='',shijian = 3600*60,price = 1000000,pic = '无'):
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
		res = all.split('/')
		#print res
		if len(res)>1:
			##取得最后一个，因为在测试时出现里地址也含有/
			#shijian = res[len(res)-1]
			shijian = res[1]
			#print 'in get_time:'
			#print shijian
			shijian = shijian.strip()
			shijians = shijian.split('-')
			#指处理，小时和分钟，对于11-11这样的日期没必要处理
			if len(shijians)==1:

				#取得中文，也就是后面的单位
				r = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\\n\\r]", "", shijian)
				#取得前面的数字
				num = filter(str.isdigit, shijian)	
				print '单位：'+r.strip()
				print '值：'+num
				r = r.strip()
				num = num.strip()
			
				#print r
				#print 'before int(num)'
				#print num
				num = int(num)
				#print 'time_num:%d'%num
				#print '单位 type'
				#print type(r)
				if r == u'分钟'.encode('utf-8') or r == u'分钟 '.encode('utf-8'):
					#print '这里是分钟'
					return num
				if r == u'小时'.encode('utf-8') or r == u'小时 '.encode('utf-8'):
					return num*60
				else:
					return 3600*60
		return 3600*3600

	def parse_58(self):
		self.__addr_infos = []
		soup = BeautifulSoup(self.__html)
		section = soup.body.find('section',id="mainlist")
		#这里的table是个列表
		table = section.find_all('table',class_='tbimg')

		#下面得到一个tag，这里是我们找到的第二个table，也就是我们需要的
		if len(table) > 1:
			realbody = table[1]
		else:		
			return ''
		##得到需要的tr列表
		tbody = realbody.tbody

		#找到所有的tr标签
		trs = tbody.find_all('tr')
		#下面开始解析需要的信息
		for tr in trs:
			info = Info()
			#找到<td class='t'>的标签
			td = tr.find('td',class_="t")
			#title
			#print '标题：'
			#print td.a.get_text().strip()
			info.title = td.a.get_text().strip()
			#href
			#print 'href'
			info.href =  td.a['href']
			#有几图  [3图]
			ntu = td.find('span',class_="ico ntu")
			#print "是否有图:"
			pic = '无'
			if ntu is not None:
				pic =  ntu.get_text()
			info.pic = pic

			#摘要
			li =  td.contents
			#print 'li len:%d'%len(li)
			description = ''
			if len(li) == 17:
				#print '摘要：'
				description =  li[8]
			i = 0
			if len(li) == 15:
				#print '摘要：'
				description =  li[6]

			fl = td.find('span',class_="fl")
			fl_all = fl.get_text()
			fl_list = fl.contents
			#print '时间：'
			fl_list_len = len(fl_list)
			#最后一项就是时间
			time_str =  fl_list[fl_list_len-1]

			#下面取得时间
			#print '时间：'
			#info.add = time_str.encode('utf-8')
			info.shijian =  self.get_58_time(time_str.encode('utf-8'))

			td = tr.find('td',class_='tc')
			#价格
			#print '价格：'
			info.price =  td.b.string
			print 'info:'
			print 'title:'+info.title
			print 'href:'+info.href

			print 'price:%s'%info.price
			print 'shijia:%d'%info.shijian
			self.__addr_infos.append(info)
		
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
	tc = tc58('http://wh.58.com/pbdn/?key=ipad')
	tc.fun_loop()

