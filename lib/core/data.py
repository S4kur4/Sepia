#!/usr/bin/env python
#-*- coding:utf-8 -*-

from lib.core.log import MY_LOGGER
from lib.core.datatype import AttribDict

logger = MY_LOGGER

paths = AttribDict() #定义新字典对象paths

cmdLineOptions = AttribDict() #定义新字典对象cmdLineOptions

conf = AttribDict() #定义新字典对象conf

th = AttribDict() #定义新字典对象th

targetlist = [] #用来存储扫描结果