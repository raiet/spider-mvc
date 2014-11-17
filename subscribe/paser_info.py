#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
     定义解析的结果
'''

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
