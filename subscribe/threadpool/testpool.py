#!/usr/bin/env python
##  coding:utf-8

from threadpool import ThreadPool
import time
def do_work(*args, **kwds):
     num = kwds['id']
     my_num = 0
     while my_num<10:
          print 'num:%d'%num
          print 'do some thing:%d'%my_num
          my_num = my_num + 1
          time.sleep(num)

# Create thread pool with nums threads
pool = ThreadPool(5)
# Add a task into pool
pool.add_task(do_work, None, id = 1)
pool.add_task(do_work, None, id = 2)
pool.add_task(do_work, None, id = 3)
# Join and destroy all threads
pool.destroy()
