#!/usr/bin/env python
#-*- coding:utf-8 -*-

import Queue
import sys
import imp
import os
from lib.core.data import th, conf, logger, paths
from lib.core.enums import TARGET_MODE_STATUS
from lib.core.settings import ESSENTIAL_MODULE_METHODS
from lib.core.exception import ToolkitValueException
from lib.controller.api import runApi
from thirdparty.IPy import IPy


def loadModule():
    _name = conf.MODULE_NAME #加载的脚本名
    msg = 'Load script: %s' % _name
    logger.info(msg)
    #在脚本文件夹中查找_name文件
    fp, pathname, description = imp.find_module(os.path.splitext(_name)[0], [paths.SCRIPT_PATH])
    try:
        th.module_obj = imp.load_module("_", fp, pathname, description) #加载找到的模块
        for each in ESSENTIAL_MODULE_METHODS: #ESSENTIAL_MODULE_METHODS=['poc']
            if not hasattr(th.module_obj, each): #如果模块中不存在'poc'方法就提醒并退出
                errorMsg = "Can't find essential method:'%s()' in current script，Please modify your script/PoC".format(each)
                sys.exit(logger.error(errorMsg))
    except ImportError, e: #模块加载失败就抛出异常
        errorMsg = "Your current scipt [%s.py] caused this exception\n%s\n%s" \
                   % (_name, '[Error Msg]: ' + str(e), 'Maybe you can download this module from pip or easy_install')
        sys.exit(logger.error(errorMsg))


def loadPayloads():
    infoMsg = 'Initialize targets...'
    logger.info(infoMsg)
    th.queue = Queue.Queue() #创建扫描目标队列
    if conf.TARGET_MODE is TARGET_MODE_STATUS.FILE: #conf.TARGET_MOD=9 -f模式
        file_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.IPMASK: #conf.TARGET_MOD=7 -c模式
        cidr_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.SINGLE: #conf.TARGET_MOD=8 -u模式
        single_target_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.API: #conf.TARGET_MOD=5 API模式
        api_mode()

    else:
        raise ToolkitValueException('conf.TARGET_MODE value ERROR.')
    logger.info('Total: %s' % str(th.queue.qsize()))


def file_mode():
    for line in open(conf.INPUT_FILE_PATH): #读取文件中的每行并丢进队列
        sub = line.strip()
        if sub:
            th.queue.put(sub)


def cidr_mode():
    ori_str = conf.NETWORK_STR
    try:
        _list = IPy.IP(ori_str) #使用IPy插件得到IP列表
    except Exception, e:
        sys.exit(logger.error('Invalid IP/MASK,%s' % e))
    for each in _list: #将IP列表丢进队列
        th.queue.put(str(each))


def single_target_mode():
    th.queue.put(str(conf.SINGLE_TARGET_STR))


def api_mode():
    conf.API_OUTPUT = os.path.join(paths.DATA_PATH, conf.API_MODE)
    if not os.path.exists(conf.API_OUTPUT):
        os.mkdir(conf.API_OUTPUT)

    file = runApi()
    for line in open(file):
        sub = line.strip()
        if sub:
            th.queue.put(sub)
