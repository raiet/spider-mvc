#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    这个模块主要解析58同城的页面

    
"""
from bs4 import BeautifulSoup
from const import HTML_PATH
import re,os

from paser_info import Info


def get_58_2_time(all):
    #取得中文，也就是后面的单位
    r = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\\n\\r]", "", all)
    #取得前面的数字
    num = filter(str.isdigit, all)

    #print u'单位:'
    #print r.strip()
    #print u'值:'
    #print num
    r = r.strip()
    #print type(r)
    num = num.strip()
    num = int(num)
    if r == u'分钟'.encode('utf-8') or r == u'分钟 '.encode('utf-8'):
        #print '这里是分钟'
        return num
    if r == u'小时'.encode('utf-8') or r == u'小时 '.encode('utf-8'):
        return num*60
    else:
        return 3600*60

##http://wh.58.com/jiajiaogeren/?key=%E8%8B%B1%E8%AF%AD		    
def parse_58_2(file_name):
    addr_infos = []
    file_path = '%s/%s'%(HTML_PATH,file_name)
    print 'path file:%s'%file_path
    html = ''
    with open(file_path,'r') as f:
        html = f.read()
    #print html
    soup = BeautifulSoup(html)
    tables = soup.find_all('table',class_="tblist tb-jjgr")
    #print 'len tables :%d'%len(tables)
    table = None
    if(len(tables)>0):
        table = tables[0]
    else:
        print 'hi cant paser here !! i am paser_58_2'
        return addr_infos
    trs = table.find_all('tr')
    #print 'len trs %d'%len(trs)
    patt = re.compile(r"\((.*?)\)", re.I|re.X)
    try:
        for tr in trs:
            info = Info()
            t2s = tr.find_all('td',class_='t')
            #print 'len t2s:%d'%(len(t2s))
            if len(t2s)>0:
                t2 = t2s[0]
                info.title = t2.a.get_text()
                info.href =  t2.a['href']
                #print info.href
                #contents = t2.contents
                #print contents
                #全部信息
                #可以进行三部分解析
                #第一部分是标题，第二部分是正文，包含时间信息，第三部分是地址
                #所以关键是解析这一段的时间
                con = str(t2.get_text().encode('utf-8'))
                info.description = con
                #print con
                #print type(con)
                #print '111111'

                all = patt.findall(con)
                #print '2222'

                t = all[len(all)-1]
                time_str = t
                time_num = get_58_2_time(time_str)
                info.shijian = time_num
                #print 'shijian:%d'%(info.shijian)
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


def get_58_1_time(all):
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
                    #print '单位：'+r.strip()
                    #print '值：'+num
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


##http://wh.58.com/pbdn/?key=ipad
def parse_58_1(file_name):
    print 'hi enter paer_58——1'
    addr_infos = []
    file_path = '%s/%s'%(HTML_PATH,file_name)
    print 'file_path:%s'%file_path
    html = ''
    try:
        with open(file_path,'r') as f:
            html = f.read()
        #print html
    except Exception ,e:
        print e
        return addr_infos
    
    soup = BeautifulSoup(html)
    section = soup.body.find('section',id="mainlist")
    if section is None:
        print 'hi   i am paser_58_1,cant paser'
        return addr_infos
    #这里的table是个列表
    table = section.find_all('table',class_='tbimg')

    #下面得到一个tag，这里是我们找到的第二个table，也就是我们需要的
    if len(table) > 1:
        realbody = table[1]
    else:
        print 'cant paser i am paser_58_1'
        return addr_infos
    try:
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
            info.shijian =get_58_1_time(time_str.encode('utf-8'))

            td = tr.find('td',class_='tc')
            #价格
            #print '价格：'
            info.price =  td.b.string
            #print 'info:'
            #print 'title:'+info.title
            #print 'href:'+info.href

            #print 'price:%s'%info.price
            #print 'shijia:%d'%info.shijian
            addr_infos.append(info)
    except Exception ,e:
        print 'i am paer_58_1,i raise a exception'
        print e
    finally:
        if len(addr_infos)>0:
            os.remove(file_path)
        return addr_infos
