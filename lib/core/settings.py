#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import subprocess

VERSION = '1.1.0'
PROJECT = "Sepia"
PLATFORM = os.name
IS_WIN = subprocess.mswindows #判断当前环境是否为Windows

# essential methods/functions in custom scripts/PoC (such as function poc())
ESSENTIAL_MODULE_METHODS = ['poc']
# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"
# String representation for NULL value
NULL = "NULL"
# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\x%02x"

ISSUES_PAGE = "https://github.com/Xyntax/POC-T/issues"
GIT_REPOSITORY = "git://github.com/Xyntax/POC-T.git"
GIT_PAGE = "https://github.com/Xyntax/POC-T"

BANNER = """\033[01;33m                _      
 ___  ___ _ __\033[01;31m(¯ω¯)\033[01;33m __ _  \033[01;37m{\033[01;33m%s\033[01;37m#dev}\033[01;33m
/ __|/ _ \ '_ \| |/ _` |
\__ \  __/ |_) | | (_| |
|___/\___| .__/|_|\__,_|  \033[07;33;41mPoC|Exploit\033[0m\033[01;33m
         |_|            
                       \033[0m\n""" % VERSION