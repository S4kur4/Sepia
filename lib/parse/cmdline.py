#!/usr/bin/env python
#-*- coding:utf-8 -*-

import argparse #argparse模块代替过时的optparse
import sys
from lib.core.settings import VERSION #setting文件定义了框架基本信息，这里导入框架版本


def cmdLineParser():
    parser = argparse.ArgumentParser(description='Example: python sepia.py -s dns_zonetransfer --zoomeye "port:8080"', add_help=False)

    #第一项optional_arguments，基础相关项
    optional_arguments = parser.add_argument_group('Options')
    optional_arguments.add_argument('-h', '--help', action='help', help='Show help message and exit')
    optional_arguments.add_argument('-v', '--version', action='version', version=VERSION, help="Show program's version number and exit")

    #第二项engine_mode，扫描引擎配置项
    engine_mode = parser.add_argument_group('Engine')
    engine_mode.add_argument('--threads', dest="engine_thread", default=False, action='store_true', help='Multi-Threaded engine (default choice)')
    engine_mode.add_argument('--gevent', dest="engine_gevent", default=False, action='store_true', help='Gevent engine (single-threaded with asynchronous)')
    engine_mode.add_argument('-t', metavar='NUMBER', dest="thread_num", type=int, default=10, help='number of threads/concurrent, 10 by default')
    
    #第三项script，脚本配置项
    script = parser.add_argument_group('Script')
    script.add_argument('-s', metavar='SCRIPT', dest="script_name", type=str, default='', help='Load script by name (-s jboss-rce) or path (-s ./script/jboss.py)')
    script.add_argument('--list', dest="list_scripts", default=False, action='store_true', #列出所有的脚本
                      help='List available script names in ./script/ and exit')
    #第四项target，扫描目标配置项
    target = parser.add_argument_group('Target')
    target.add_argument('-u', '--url', metavar='URL', dest="target_url", type=str, default='', help='Target URL (e.g. http://www.targetsite.com/)')
    target.add_argument('-f', '--file', metavar='URLFILE', dest="target_file", type=str, default='', help='Load targets from targetFile (e.g. ./data/wooyun_domain)')
    target.add_argument('-c', '--cidr', metavar='CIDR', dest="target_cidr", type=str, default='', help='Read a CIDR (e.g. 10.0.1.0/24)')

    #第四项api，扫描数据接口配置项
    api = parser.add_argument_group('API')
    api.add_argument('-zoomeye', metavar='DORK', dest="zoomeye_dork", type=str, default='', help='ZoomEye dork (e.g. "zabbix port:8080")')
    api.add_argument('-baidu', metavar='DORK', dest="baidu_dork", type=str, default='', help='Baidu dork (e.g. "inurl:login.action")')
    api.add_argument('--limit', metavar='NUMBER', dest="api_limit", type=int, default=10, help='Maximum searching results (default:10)')
    api.add_argument('--offset', metavar='OFFSET', dest="api_offset", type=int, default=0, help="Search offset to begin getting results from (default:0)")
    api.add_argument('--search-type', metavar='TYPE', dest="search_type", action="store", default='host', help="[ZoomEye] search type used in ZoomEye API, web or host (default:host)")
    if len(sys.argv) == 1:
        sys.exit('sepia.py: error: missing a mandatory option (-s, -u|-f|-c|-zoomeye|-baidu), use -h for help')
        sys.argv.append('-h')
    args = parser.parse_args()
    return args
