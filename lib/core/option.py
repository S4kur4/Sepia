#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import glob #文件路径查找
import sys
from lib.core.data import conf, paths, th, logger
from lib.core.enums import TARGET_MODE_STATUS, ENGINE_MODE_STATUS
from lib.core.enums import API_MODE_NAME
from lib.core.register import Register
from lib.core.common import dataToStdout
from thirdparty.prettytable.prettytable import PrettyTable


def initOptions(args): #初始化操作
    checkShow(args) #检查是否要求列出脚本
    checkSearch(args) #检查是否在搜索脚本
    EngineRegister(args) #检查配置扫描引擎，注册互斥量，扫描线程数
    ScriptRegister(args) #检查配置脚本项参数
    TargetRegister(args) #检查配置扫描目标信息
    ApiRegister(args) #检查API配置信息
    '''
    print "#########以下是conf字典#########"
    print conf
    '''

def checkShow(args):
    input_path = args.script_name
    list_scripts = args.list_scripts
    search_script = args.search_script
    if list_scripts and (input_path or search_script):
        msg = 'Cannot specify or search script when you use [--list]'
        sys.exit(logger.error(msg))
    scriptsheet = PrettyTable(["Script"])
    scriptsheet.align["Script"] = "l"
    scriptsheet.padding_width = 1
    if list_scripts:
        module_name_list = glob.glob(os.path.join(paths.SCRIPT_PATH, '*.py')) #获取script文件夹下所有.py文件列表
        msg = 'Total:{}\n'.format(str(len(module_name_list) - 1)) #除去__init__.py算出total总数
        for each in module_name_list:
            _str = os.path.split(each)[1][0:-3]
            if _str != '__init__':
                scriptsheet.add_row([_str])
        print scriptsheet
        dataToStdout(msg)
        logger.info('System exit')
        sys.exit()

def checkSearch(args):
    input_path = args.script_name
    list_scripts = args.list_scripts
    search_script = args.search_script
    if search_script and (input_path or list_scripts):
        msg = 'Cannot specify or list script when you use [--search]'
        sys.exit(logger.error(msg))
    if search_script:
        if re.findall(r'[^\w\d\-_ ]', search_script):
            msg = 'The script name you provided is incorrect'
            sys.exit(logger.error(msg))
        scriptsheet = PrettyTable(["Script"])
        scriptsheet.align["Script"] = "l"
        scriptsheet.padding_width = 1
        length = 0
        module_name_list = glob.glob(os.path.join(paths.SCRIPT_PATH, '*.py'))
        for each in module_name_list:
            _str = os.path.split(each)[1][0:-3]
            if _str != '__init__' and re.findall(search_script, _str):
                scriptsheet.add_row([_str])
                length = length + 1
        if length > 0:
            msg = 'Total:{}\n'.format(length)
            print scriptsheet
            dataToStdout(msg)
        else:
            msg = 'No results found'
            logger.error(msg)
        logger.info('System exit')
        sys.exit()


def EngineRegister(args):
    thread_status = args.engine_thread
    gevent_status = args.engine_gevent
    thread_num = args.thread_num

    def __thread():
        conf.ENGINE = ENGINE_MODE_STATUS.THREAD #Thread=9

    def __gevent():
        conf.ENGINE = ENGINE_MODE_STATUS.GEVENT #Gevent=8

    conf.ENGINE = ENGINE_MODE_STATUS.THREAD  # default choice Thread=9

    msg = 'Use [--threads] to set Multi-Threaded mode or [--gevent] to set Coroutine mode.'
    r = Register(mutex=True, start=0, stop=1, mutex_errmsg=msg)
    r.add(__thread, thread_status)
    r.add(__gevent, gevent_status)
    r.run()

    if 0 < thread_num < 101:
        th.THREADS_NUM = conf.THREADS_NUM = thread_num
    else:
        msg = 'Invalid input in [--number], range: 1 to 100'
        sys.exit(logger.error(msg))


def ScriptRegister(args):
    input_path = args.script_name
    list_scripts = args.list_scripts
    search_script = args.search_script
    # handle input: nothing
    if input_path and (search_script or list_scripts):
        msg = 'Cannot specify script when you use [--list] or [--search]'
        sys.exit(logger.error(msg))
    # handle input: "-s ./script/spider.py"
    if input_path:
        if os.path.split(input_path)[0]: #如果指定了脚本获取给出脚本的文件夹路径
            if os.path.exists(input_path): #判断是否存在该脚本文件
                if os.path.isfile(input_path): #判断是否是文件
                    if input_path.endswith('.py'): #判断是否是Python文件
                        conf.MODULE_NAME = os.path.split(input_path)[-1] #得到脚本文件名.py
                        conf.MODULE_FILE_PATH = os.path.abspath(input_path) #得到脚本文件的绝对路径
                    else:
                        msg = '[%s] not a Python file. Example: [-s spider] or [-s ./script/spider.py]' % input_path
                        sys.exit(logger.error(msg))
                else:
                    msg = '[%s] not a file. Example: [-s spider] or [-s ./script/spider.py]' % input_path
                    sys.exit(logger.error(msg))
            else:
                msg = '[%s] not found. Example: [-s spider] or [-s ./script/spider.py]' % input_path
                sys.exit(logger.error(msg))

    # handle input: "-s spider"  "-s spider.py"
        else:
            if not input_path.endswith('.py'): #如果指定的脚本文件不以.py结尾就加一个.py
                input_path += '.py'
            _path = os.path.abspath(os.path.join(paths.SCRIPT_PATH, input_path))
            if os.path.isfile(_path): #如果这个脚本文件在脚本库中找不到就提醒并退出
                conf.MODULE_NAME = input_path
                conf.MODULE_FILE_PATH = os.path.abspath(_path)
            else:
                msg = 'Script [%s] not exist. Use [--list] to view all available scripts in ./script/' % input_path
                sys.exit(logger.error(msg))


def TargetRegister(args):
    input_path = args.script_name
    input_file = args.target_file
    input_single = args.target_urlip
    input_cidr = args.target_cidr
    api_zoomeye = args.zoomeye_dork
    api_baidu = args.baidu_dork

    if not input_path:
        msg = 'Please specify a script with [-s]'
        sys.exit(logger.error(msg))
    def __file(): #配置批量扫描文件路径
        if not os.path.isfile(input_file):
            msg = 'TargetFile not found: %s' % input_file
            sys.exit(logger.error(msg))
        conf.TARGET_MODE = TARGET_MODE_STATUS.FILE #conf.TAGET_MODE=9 -iF模式
        conf.INPUT_FILE_PATH = input_file

    def __cidr():
        conf.TARGET_MODE = TARGET_MODE_STATUS.IPMASK #conf.TARGET_MODE=7 -iN模式
        conf.NETWORK_STR = input_cidr
        conf.INPUT_FILE_PATH = None

    def __single():
        conf.TARGET_MODE = TARGET_MODE_STATUS.SINGLE #conf.TARGET_MODE=8 -iS模式
        conf.SINGLE_TARGET_STR = input_single
        th.THREADS_NUM = conf.THREADS_NUM = 1
        conf.INPUT_FILE_PATH = None

    def __zoomeye():
        conf.TARGET_MODE = TARGET_MODE_STATUS.API #conf.TARGET_MODE=5 API模式
        conf.API_MODE = API_MODE_NAME.ZOOMEYE #使用Zoomeye
        conf.API_DORK = api_zoomeye

    def __baidu():
        conf.TARGET_MODE = TARGET_MODE_STATUS.API #conf.TARGET_MODE=5 API模式
        conf.API_MODE = API_MODE_NAME.BAIDU #使用Baidu
        conf.API_DORK = api_baidu

    msg = 'Please load targets with [-t|-f|-c] or use API with [-zoomeye|-baidu]'
    r = Register(mutex=True, mutex_errmsg=msg)
    r.add(__file, input_file)
    r.add(__cidr, input_cidr)
    r.add(__single, input_single)
    r.add(__zoomeye, api_zoomeye)
    r.add(__baidu, api_baidu)
    r.run()


def ApiRegister(args):
    search_type = args.search_type
    offset = args.api_offset
    api_limit = args.api_limit

    if not 'API_MODE' in conf:
        return

    if not conf.API_DORK:
        msg = 'Empty API dork, show usage with [-h]'
        sys.exit(logger.error(msg))

    if offset < 0:
        msg = 'Invalid value in [--offset], show usage with [-h]'
        sys.exit(logger.error(msg))
    else:
        conf.API_OFFSET = offset

    if api_limit <= 0:
        msg = 'Invalid value in [--limit], show usage with [-h]'
        sys.exit(logger.error(msg))
    else:
        conf.API_LIMIT = api_limit

    if conf.API_MODE is API_MODE_NAME.ZOOMEYE:
        if search_type not in ['web', 'host']:
            msg = 'Invalid value in [--search-type], show usage with [-h]'
            sys.exit(logger.error(msg))
        else:
            conf.ZOOMEYE_SEARCH_TYPE = search_type
