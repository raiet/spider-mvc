spider-mvc
==========

学习python之后的一个总结，主要实现了定向抓取58同城和赶集网，同时使用了mvc的架构搭了一个界面

1，目录说明
==========



- html_file:抓取的页面的临时缓存文件夹，解析完毕或是解析失败之后都会清空

- subscribe：抓取，解析和发送邮件（在里面没有实现，只是用写文件代替你了具体的简单实现，可以[参考这里](https://github.com/raiet/58-python-spider)）

- www:web程序目录，这个是参考的[廖学锋的的一个mvc-diy框架](),个人觉的，看了这个框架，使我对python编程有了一个新的认识，之前都是用java写的mvc，发现用python写也是这么简单。
- setup.py，运行整个服务
- weixin.sql 数据库的scheme文件

- pymonitor.py,开发时的监控程序，在开发过程中，可以运行这个文件，达到一个应用热部署的效果（其实就是检测文件是否有过变动，如果有变动们就会重启整个服务）

2，运行

	python setup.py pymonitor.py

3，运行效果

![界面](/www/static/3.png "首页")
![界面](/www/static/2.png "添加")
![界面](/www/static/1.png "详细")

4，开始使用吧！！