#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
     这个模块主要是解析赶集网的页面
'''


import re,os

from paser_info import Info
from bs4 import BeautifulSoup


from const import HTML_PATH


def get_ganji_1_time(all):
     ##这里对于某月某日的日期实际上是不处理的，因为那些时间至少是一天以前的，没哟必要处理
     ##则可以返回一个很大的时间
     #print 'in get_time'
     #print type(all)
     #取得中文，也就是后面的单位
     r = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\\n\\r]", "", all)
     #取得前面的数字
     num = filter(str.isdigit, all)

     #print '单位：'+r.strip()
     #print '值：' + num
     ##有些记录就没有时间这一项，比如以商家来代替时间
     ##所以对于这种情况，直接返回最大的时间
     if len(num)==0:
          return 3600*60
     r = r.strip()
     #print 'len (r):%d'%len(r)
     #print 'len(u分钟):%d'%len(u'分钟'.encode('utf-8'))
     num = num.strip()
     num = int(num)

     if r == u'分钟'.encode('UTF-8') or r == u'分钟 '.encode('utf-8'):
          #print '这里是分钟'
          return num
     elif r == u'小时'.encode('utf-8') or r == u'小时 '.encode('utf-8'):
          #print '这里是小时'
          return num*60
     else:
          #print '什么都没有匹配到'
          return 3600*60

     
##http://wh.ganji.com/ipadpingban/?original=ipad
def parse_ganji_1(file_name):
     addr_infos = []
     file_path = '%s/%s'%(HTML_PATH,file_name)
     print 'path file:%s'%file_path
     html = ''
     with open(file_path,'r') as f:
          html = f.read()
     #print html
     soup = BeautifulSoup(html)
     tables = soup.find_all('div',class_="layoutlist")
     #print len(tables)

     table = None
     if(len(tables)>0):
          table = tables[0]
     else:
          print 'hi i am paser_gan_1 cant paser'
          return addr_infos
     try:
          trs = table.find_all('dl')
          patt = re.compile(r"\((.*?)\)", re.I|re.X)
          for tr in trs:
               info = Info()
               t2s = tr.find_all('dd',class_='feature')
               if len(t2s)>0:
                    t2 = t2s[0]
                    li = t2.find_all('li',class_="js-item")
                    #print 'len(li):%d'%len(li)
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
                         #print "*"*30
                         #print 'time_str'
                         #print time_str
                         
                         info.shijian = get_ganji_1_time(time_str.encode('UTF-8'))

                    #print 'info:'
                    #print 'title:'+info.title
                    #print 'href:'+info.href
                    #print 'price:%s'%info.price
                    #print 'shijia:%d'%info.shijian
                    addr_infos.append(info)
                    
     except Exception ,e:
          print e
     finally:
          if len(addr_infos)>0:
               os.remove(file_path)
          return addr_infos
