#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    这里主要做url的映射，接受用户请求
'''
__author__ = 'hustraiet@gmail.com'

import os, re, time, base64, hashlib, logging,sys

import markdown2

from transwarp.web import get, post, ctx, view, interceptor, seeother, notfound

from apis import api, Page, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from models import User, Blog, Comment,Url,Unactiveurl,Users
from config import configs
sys.path.append('..')
_COOKIE_NAME = 'matrixsession'
_COOKIE_KEY = configs.session.secret

def _get_page_index():
    page_index = 1
    try:
        page_index = int(ctx.request.get('page', '1'))
    except ValueError:
        pass
    return page_index

def make_signed_cookie(id, email, max_age):
    # build cookie string by: id-expires-md5
    expires = str(int(time.time() + (max_age or 86400)))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, email, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L)

def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = Users.get(id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.email, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except:
        return None

def check_admin():
    user = ctx.request.user
    if user and user.admin:
        return
    raise APIPermissionError('No permission.')

@interceptor('/')
def user_interceptor(next):
    logging.info('try to bind user from session cookie...')
    user = None
    cookie = ctx.request.cookies.get(_COOKIE_NAME)
    if cookie:
        logging.info('parse session cookie...')
        user = parse_signed_cookie(cookie)
        if user:
            logging.info('bind user <%s> to session...' % user.email)
    ctx.request.user = user
    return next()

@interceptor('/manage/')
def manage_interceptor(next):
    user = ctx.request.user
    if user and user.admin:
        return next()
    raise seeother('/signin')

@interceptor('/index')
def index_interceptor(next):
    logging.info('try to check user from session cookie...')
    user = ctx.request.user
    if user is not None:
        logging.info('user is not None...')
        return next()
    raise seeother('/signin')

@view('show.html')
@get('/index')
def index():
    user=ctx.request.user
    urls, page = _get_urls_by_user_and_page(user.id)
    return dict(page=page, urls=urls, user=ctx.request.user)

@view('single_url.html')
@get('/index/url/:url_id')
def show_single_url(url_id):
    url = Url.get(url_id)    
    return dict(url=url, user=ctx.request.user)


@view('signin.html')
@get('/signin')
def signin():
    return dict()


@view('add_url.html')
@get('/index/add_url')
def add_url():
    return dict(user=ctx.request.user)


@get('/signout')
def signout():
    ctx.response.delete_cookie(_COOKIE_NAME)
    raise seeother('/index')

@api
@post('/api/authenticate')
def authenticate():
    i = ctx.request.input(remember='')
    email = i.email
    tel = i.tel
    remember = i.remember
    user = Users.find_first('where email=? and tel = ?', email,tel)
    if user is None:
        raise APIError('auth:failed', 'email', 'Invalid email or tel.')
    # make session cookie:
    max_age = 604800 if remember=='true' else None
    print '111'
    cookie = make_signed_cookie(user.id, user.email, max_age)
    print '222'
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
    print '333'
    user.tel = '******'
    return user

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_TOP_NUM = re.compile(r'^[0-9]{1,3}$')
_RE_FREQUENT = re.compile(r'^[0-9]*$')
_RE_TEL = re.compile(r'^[0-9]{11}$')


@api
@post('/api/users')
def register_user():
    i = ctx.request.input(email='', tel='')
    email = i.email.strip().lower()
    tel = i.tel
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not tel or not _RE_TEL.match(tel):
        raise APIValueError('tel')
    user = User.find_first('where email=?', email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = Users(email=email, tel=tel)
    user.insert()
    # make session cookie:
    cookie = make_signed_cookie(user.id, user.email, None)
    ctx.response.set_cookie(_COOKIE_NAME, cookie)
    return user

@view('register.html')
@get('/register')
def register():
    return dict()

def _get_urls_by_user_and_page(user_id):
    total = Url.count_all()
    page = Page(total, _get_page_index())
    urls = Url.find_by("where user_id = ?and `status` != 2 order by create_time desc limit ?,?",user_id, page.offset, page.limit)
    return urls, page
@api
@post('/api/url')
def api_add_url():
    #check_admin()
    i = ctx.request.input(url='', frequent='', top_num='',summary = '')
    url = i.url.strip()
    frequent = i.frequent.strip()
    top_num = i.top_num.strip()
    summary = i.summary
    if not url:
        raise APIValueError('url', 'url cannot be empty.')
    if frequent and not _RE_FREQUENT.match(frequent):
        raise APIValueError('frequent', 'frequent MUST be num. or empty')
    if top_num and not _RE_TOP_NUM.match(top_num):
        raise APIValueError('top_num', 'top_num must be 1-999  or empty.')
    user = ctx.request.user
    if frequent == '':
        frequent = 30
    
    if top_num == '':
        top_num = 1
    url = Url(user_id=user.id, url = url,frequent=frequent, top_num=top_num,summary = summary)
    url.insert()
    return url
##当前url不能解析，需要关闭
def close_url(url):
    print '[close_url]:%s'%url.id
    #改变当前状态改为删除
    url.status = 2
    ##清空当前的新纪录
    url.record_contents = ''
    url.new_record_num = 0
    url.reason = '用户主动取消，欢迎继续使用^_^'
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
   
@view('show.html')
@get('/index/delete/:url_id')
def delete_url(url_id):
    #check_admin()
    url = Url.get(url_id)
    if url is None:
        raise APIResourceNotFoundError('url')
    close_url(url)
    raise seeother('/index')

@view('show.html')
@get('/index/open/:url_id')
def open_url(url_id):
    #check_admin()
    url = Url.get(url_id)
    if url is None:
        raise APIResourceNotFoundError('url')
    ##之前不是关闭状态
    if url.status != 0:
        raise APIResourceNotFoundError('url')
    url.status = 1
    url.update()
    raise seeother('/index')

@view('show.html')
@get('/index/close/:url_id')
def close_url(url_id):
    #check_admin()
    url = Url.get(url_id)
    if url is None:
        raise APIResourceNotFoundError('url')
    ##之前不是关闭状态
    if url.status != 1:
        raise APIResourceNotFoundError('url')
    url.status = 0

    ##todo:这里还有很多事情要做，比如关闭监听，需要删除之前抓的网页
    url.update()
    raise seeother('/index')
