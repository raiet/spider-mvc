Thread pool
============
这是一个简单的线程池的实现，使用了简单的线程模型.


Usage:
============

- 首先，你需要定义一个用于处理任务的函数函数


        def do_work(*args, **kwds):
            # do something
        
- 之后，你就可以创建线程池，来执行任务了
    
        from threadpool import ThreadPool
        # Create thread pool with nums threads
        pool = ThreadPool(nums)
        # Add a task into pool
        pool.add_task(do_work, args, kwds)
        # Join and destroy all threads
        pool.destroy()
    
