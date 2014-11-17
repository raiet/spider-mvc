#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'hustraiet'

'''
Models for users, activeurl, unactiveurl.
'''

import time, uuid,datetime

from transwarp.db import next_id
from transwarp.orm import Model, StringField,IntegerField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


def now_datetime():
    now = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
				
    return now
                                           
class User(Model):
    __table__ = 'users'

    id = StringField(updatable=False,primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updatable=False, ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(updatable=False, default=time.time)


class Users(Model):
    __table__ = 'users'

    id = StringField(updatable=False,primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updatable=False, ddl='varchar(50)')
    tel = StringField(ddl='varchar(50)')
    admin = BooleanField()
    status = BooleanField()
    create_time= StringField(default =now_datetime)

    
class Blog(Model):
    __table__ = 'blogs'

    id = StringField(updatable=False,primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)

class Url(Model):
    __table__='activeurl'

    id = StringField(updatable=False,primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    url = StringField(ddl='varchar(255)')
    frequent = IntegerField(updatable=False, default=30)
    top_num = IntegerField(updatable=False, default=1)
    send_mail_num = IntegerField(updatable=True, default=0)
    total_record_num = IntegerField(updatable=True, default=0)
    get_page_num = IntegerField(updatable=True, default=0)
    parse_page_num = IntegerField(updatable=True, default=0)
    new_record_num = IntegerField(updatable=True, default=0)
    record_contents = TextField()
    last_send_time = StringField()
    create_time= StringField(default =now_datetime)
    status = IntegerField(updatable=True, default=1)
    fun_index = IntegerField(updatable=True, default=0)
    summary = StringField(ddl='varchar(255)')
    reason = StringField(ddl='varchar(1024)',default = r'一切正常')
    last_time = IntegerField(updatable=True, default=0)
    

class Unactiveurl(Model):
    __table__='unactiveurl'

    id = StringField(updatable=False,primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    url = StringField(ddl='varchar(255)')
    frequent = IntegerField(updatable=False, default=30)
    top_num = IntegerField(updatable=False, default=1)
    send_mail_num = IntegerField(updatable=True, default=0)
    total_record_num = IntegerField(updatable=True, default=0)
    get_page_num = IntegerField(updatable=True, default=0)
    parse_page_num = IntegerField(updatable=True, default=0)
    new_record_num = IntegerField(updatable=True, default=0)
    record_contents = TextField()
    last_send_time = StringField(default =now_datetime)
    create_time= StringField(default =now_datetime)
    
					   

class Comment(Model):
    __table__ = 'comments'

    id = StringField(updatable=False,primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(updatable=False, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)
