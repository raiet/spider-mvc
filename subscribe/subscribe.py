#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    这个模块主要完成网页抓取，分析，发邮件，使用多线程实现
    
"""



##映入配置常数
from const import GRAB_NUM,PASER_NUM,MAIL_SENDER_NUM,HTML_PATH
from const import GRAB_SLEEP_TIME,PASER_SLEEP_TIME,SENDER_SLEEP_TIME



import urllib2,os, sys,time,re,json,datetime
import logging; logging.basicConfig(level=logging.WARNING)

sys.path.append("..")
#引入线程池
from threadpool import ThreadPool
##引入model，实现连接数据库
from www.models import Url


from www.transwarp import db
from www.config import configs

##引入解析网页相关
from paser_info import Info
from paser_58 import parse_58_2,parse_58_1
from paser_ganji import parse_ganji_1


##全局的解析函数列表，如果添加新的解析方法，需要引入之后，并添加到这个list
paser_fun = [parse_58_1,parse_58_2,parse_ganji_1]





##两个参数 ：build_opener 对象和url对象
def load_page(opener,url):
    file_name = '%s%s%d-%s.html'%(HTML_PATH,os.path.sep,time.time(),url.id)
    ##print file_name
    f = None
    html_file = None
    try:
        f = opener.open(url.url)
        html = f.read()    
        html_file = open(file_name,'w')
        html_file.write(html)
    except Exception ,e:
        print e
        ##打开时出现异常在关闭当前请求
        logging.warning('[load page] error：%s'%e)
        close_url(url)
    finally:       
        f.close()
        html_file.close()


##hash函数，将url的id的字符串hash䌂一个数字，进行整除运算
def sdbm_hash_string(str):
    h = 0
    m = (1 << 32)
    for i in str:
        t = h
        h = (t << 6) % m + (t << 16) % m - t + ord(i)
        h %= m
    return h


##抓取网页的work函数
def do_grab(*args, **kwds):
    num = kwds['id']
    print 'i am do_grab ,No.%d\n'%num
    opener = urllib2.build_opener()
    while True:
        #print num_str*10
        total = Url.count_by("where `status` = 1")
        start = 0
        step = 100
        while(start <= total ):           
            urls = Url.find_by("where `status` = 1 order by create_time desc limit ?,?",start, step)
            for url in urls:
                if sdbm_hash_string(url.id)%num == 0:
                    ##不要让页面积压的太多
                    if url.get_page_num < (url.parse_page_num + 5):
                        try:
                            load_page(opener,url)
                            url.get_page_num = url.get_page_num+1
                            
                            url.update()
                        except Exception, e:
                            logging.warning('load_page[%s] error at %d\n%s'%(url.url,time.time(),e))
                        
            start = start+step
        time.sleep(GRAB_SLEEP_TIME)

##当前url不能解析，需要关闭
def close_url(url):
    print '[close_url]:%s'%url.id
    #改变当前状态改为未激活
    url.status = 0
    ##清空当前的新纪录
    url.record_contents = ''
    url.new_record_num = 0
    url.reason = '当前记录出现异常，将不能继续处理，程序猿们正在加班加点的为您处理，敬请谅解'
    url.update()

    ##删除已经抓取的文件
    file_list = os.listdir(HTML_PATH)
    for file_name in file_list:
        names = file_name.split('-')
        if(len(names)<2):
            continue
        url_id = names[1]
        url_id = url_id[0:-5]
        print url_id
        if url_id == url.id:
            file_path = '%s%s%s'%(HTML_PATH,os.path.sep,file_name)
            logging.info('[delete file] %s'%file_path)
            os.remove(file_path)
    
##json的自定义对象的转换
def convert(obj):
    d = {  }
    d.update(obj.__dict__)
    return d
##对自定义对象进行编码
def utf8_info(info):
    #print '3333'
    #info.description = info.description.encode('utf-8')
    #print '1'
    #info.pic = info.pic.encode('utf-8')
    #print '2'
    #info.title = info.title.encode('utf-8')
    #print '3'
    
    return info
##更新解析的内容
def update_content(url,infos):
    try:
        if len(infos)<1:
            return
        ##将last_time进行微调
        last_time = float(url.last_time) + float(PASER_SLEEP_TIME/60.0)
        #如果是第一次，则只计算last_time
        min_time = infos[0].shijian
        if url.last_time == 0:
            for info in infos:
                if info.shijian<min_time:
                    min_time = info.shijian
            url.last_time = min_time
            url.update()
            return
        min_time = last_time
        contents = None
        if url.record_contents == '' or url.record_contents is None:
            contents = []
        else:
            contents = json.loads(url.record_contents)
        
        for info in infos:
            info = utf8_info(info)
            info_dic = json.dumps(info,default = convert)
            #print info.shijian
            #print info_dic
            if info.shijian<last_time:
                contents.append(info_dic)
                if info.shijian<min_time:
                    min_time = info.shijian
        
        #print '555'
        jsoncontents = json.dumps(contents)
        url.record_contents = jsoncontents
        url.new_record_num = url.new_record_num + len(infos)
        print 'update content _to db'
        #print url.record_contents
        logging.warning('%s--update content:%s'%(url.id,url.record_contents))
        url.update()
    except Exception,e:
        print '**'*20
        print e
    


##解析网页的work函数
def do_paser(*args, **kwds):
    num = kwds['id']
    print 'i am do_paser ,No.%d\n'%num
    while True:
        file_list = os.listdir(HTML_PATH)
        for file_name in file_list:
            names = file_name.split('-')
            if(len(names)<2):
                continue
            url_id = names[1]
            url_id = url_id[0:-5]
            print '[paser]:%s'%url_id
            url = Url.get(url_id)
            if url is None:
                close_url(url)
            ##还没有检测出使用的函数，则这里检测
            url.fun_index = int(url.fun_index)
            print 'type(url.fun_index)'
            print type(url.fun_index)
            if url.fun_index == 0:
                print 'here i will to dectect which function to paser'
                for index,paser in enumerate(paser_fun):
                    #print 'here'
                    ##返回的是解析到的结果
                    infos = paser(file_name)
                    print 'len info:%d'%(len(infos))
                    ##已经检测到了结果
                    if len(infos)>0:
                        print 'ok! fun[%d] can paser it '%(index+1)
                        url.fun_index = index +1
                        update_content(url,infos)
                        print 'break'
                        break
                if(url.fun_index == 0):                    
                    ##都检测了一遍还是不能解析，则将当前的url的状态变为停止，并给出原因
                    print 'sorry! all cant paser the url,and close it'
                    close_url(url)
            else:
                print 'use fun[%d] to paser %s'%(url.fun_index,url.id)
                infos = paser_fun[url.fun_index-1](file_name)
                if len(infos)>0:
                    update_content(url,infos)

        ##线程程挂起
        time.sleep(PASER_SLEEP_TIME)

##这里真正发送邮件
def send_mail(url):
    #contents = json.loads(url.record_contents)
    file_path = '%s%smail%s%d-%s.txt'%(HTML_PATH,os.path.sep,os.path.sep,time.time(),url.id)
    f = open(file_path,'w')
    f.write(url.record_contents)
    f.close()
    ##发送完之后更新记录
    url.last_send_time = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    url.new_record_num = 0
    url.record_contents = ''
    url.update()
    

##发送邮件的work函数
def do_send(*args, **kwds):
    num = kwds['id']
    print 'i am do_send ,No.%d\n'%num
    while True:
        #print num_str*10
        total = Url.count_by("where `status` = 1 and new_record_num > 0")
        start = 0
        step = 20
        while(start <= total ):          
            urls = Url.find_by("where `status` = 1 and new_record_num > 0 order by create_time desc limit ?,?",start, step)
            for url in urls:
                #现在你开始处理
                if sdbm_hash_string(url.id)%num == 0:
                    print 'type(url.last_send_time)'
                    print type(url.last_send_time)
                    print url.last_send_time
                    ##取得上次发送的时间
                    time_num = time.mktime(time.strptime(str(url.last_send_time),'%Y-%m-%d %H:%M:%S'))
                    #time_num = time.mktime(url.last_send_time)
                    ##当前时间
                    time_now = time.time()
                    if (time_num + url.frequent*60)>time_now:
                        ##时间超过了需要发送
                        if url.new_record_num > 0:
                            send_mail(url)
                    ##如果执行了上一步，会将new_record_num 清空，所以不会执行这里
                    if url.new_record_num > url.top_num:
                        send_mail(url)
            start = start+step                   
        time.sleep(SENDER_SLEEP_TIME)
          

def run():

    
    logging.info('start subscribe server.....')

    
    ##创建抓取网页的线程池
    grab_pool = ThreadPool(GRAB_NUM)
    for i in range(GRAB_NUM):
        grab_pool.add_task(do_grab,None,id = i+1)
        
    ##创建解析网页的线程池
    paser_pool = ThreadPool(PASER_NUM)
    for i in range(PASER_NUM):
        paser_pool.add_task(do_paser,None,id = i+1)

        
    ##创建发送邮件的线程池
    send_pool = ThreadPool(MAIL_SENDER_NUM)
    for i in range(MAIL_SENDER_NUM):
        send_pool.add_task(do_send,None,id = i+1)

    # Join and destroy all threads
    grab_pool.destroy()
    paser_pool.destroy()
    send_pool.destroy()


if __name__ == '__main__':
    # init db:
    db.create_engine(**configs.db)
    run()

    

