#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    用于启动整个服务

"""
from www import wsgiapp

from subscribe import subscribe

def run():
     wsgiapp.run()
     subscribe.run()

if __name__ == '__main__':
     run()
