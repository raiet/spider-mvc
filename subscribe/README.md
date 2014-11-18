README
==

subscribe文件夹，主要功能是抓取和解析网页，有新纪录时发送邮件，使用了多线程来实现

#1，const.py

这里主要是多线程相关的配置，比如，需要开多少个线程来完成抓取任务，多少个线程完成解析任务，多少个线程完成发送邮件的任务，以及每个任务的while时的挂起时间，以合理的使用计算机资源
`HTML_PATH`，用来指定`html_file`的位置

##2，paser_info.py

定义了解析结果的对象，所有的解析程序只要将网页解析成这个结果，就可以统一处理（其中的有些字段可以不用）

##3，paser\_58.py和paser\_ganji.py
其实主要是这几个文件实现了解析功能，其中提供一个函数，工线程中回调就可以了，这个函数需要一个参数，那就是数据库activeurl表的对象，这个对象定义在`www/models.py`中

##4，threadpool文件夹
实现了一个简单的线程池，具体详见[threadpool/README.MD](threadpool/README.md)

##5，subscribe.py
这里是这个模块的主入口，这里会调用上面的所有模块。

主要结构如下：
	
	##全局的解析函数列表，如果添加新的解析方法，需要引入之后，并添加到这个list
paser_fun = [parse_58_1,parse_58_2,parse_ganji_1]
	##两个参数 ：build_opener 对象和url对象
	def load_page(opener,url):
		#根据url加载页面并存放至指定文件夹
	
	
	##hash函数，将url的id的字符串hash䌂一个数字，进行整除运算
	def sdbm_hash_string(str):
	
	
	##抓取网页的work函数，主要思路就是每个线程只处理可以被自己整出的ID
	def do_grab(*args, **kwds):
		##这里就是自己的ID
	    num = kwds['id']
	    while True:
	        while(start <= total ):  
			##从数据库中得到所有的可处理记录         
	            urls = Url.find_by("where `status` = 1 order by create_time desc limit ?,?",start, step)
	            for url in urls:
	                if sdbm_hash_string(url.id)%num == 0:
	                    ##不要让页面积压的太多
	                    if url.get_page_num < (url.parse_page_num + 5):
	                         	load_page(opener,url)
	                            url.get_page_num = url.get_page_num+1	                            
	                            url.update()
	                        
	            start = start+step
	        time.sleep(GRAB_SLEEP_TIME)
	
	##当前url不能解析，需要关闭
	def close_url(url):
		#将当前的url的状态标记为飞激活状态，
		##同时删除相关的文件

	##更新解析的内容
	def update_content(url,infos):
	    ##将新的内容存进数据库
		##如果是第一次更新，则只是计算last_time
		##也就是初始化，发送邮件的起始值
	    
	
	
	##解析网页的work函数，源码，这里有bug，本来是每个线程只处理能被自己整除的id的文件，请修改之
	def do_paser(*args, **kwds):
		##读取目录县的所有文件名，挨个解析
	    while True:
				##这里会记录使用的函数的index，0为初始化的值，表示当前记录还没有找到合适处理的函数
	            if url.fun_index == 0:
	                ##侦探可以处理的函数
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
	    
	
	##发送邮件的work函数，同do_paser bug
	def do_send(*args, **kwds):

	          
	
	def run():
	    
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
	

