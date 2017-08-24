#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import sys
import urllib
import urllib2
from urlparse import urlparse, urlunsplit, urljoin
from lib.core.common import getSafeExString
from lib.core.enums import PROXY_TYPE
from lib.utils.config import ConfigFileParser
from lib.core.data import logger, conf
from bs4 import BeautifulSoup as BS

def get_domain(url):
    p = urlparse(url)
    return urlunsplit([p.scheme, p.netloc, '', '', ''])

def iterate_path(ori_str):
    parser = urlparse(ori_str)
    _ans_list = [ori_str]
    _ans_list.append(get_domain(ori_str))
    _path_list = parser.path.replace('//', '/').strip('/').split('/')
    s = ''
    for each in _path_list:
        s += '/' + each
        _ans_list.append(urljoin(ori_str, s))
    return _ans_list

def BaiduSearch(query, limit=10, offset=0):
    urllist = {''}
    regex = str(ConfigFileParser().UrlFilter())
    try:
        while len(urllist)<limit:
            url = "http://www.baidu.com/s?{}".format(urllib.urlencode({'wd':query,'pn':str(offset)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}))
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            html = response.read()
            soup = BS(html, "lxml")
            td = soup.find_all(class_='f')
            for t in td:
                if regex:
                    after_url = re.findall(regex, t.h3.a['href'])
                    if after_url:
                        urllist.add(after_url[0])
                else:
                    after_url = iterate_path(t.h3.a['href'])
                    for each_url in after_url:
                        urllist.add(each_url)
            offset = offset + 1
        return urllist
    except urllib2.URLError, e:
        logger.warning('It seems like URL is wrong')
        sys.exit(logger.error(getSafeExString(e)))
