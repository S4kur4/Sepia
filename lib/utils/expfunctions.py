#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from lib.core.data import logger

def rce(exp, url): # Remote code excute
    logger.info("Input system command to execute or print 'q' to exit")
    command = raw_input("\033[4mCommand\033[0m > ")
    while command != "q":
        try:
            exp(url, command)
        except Exception, e:
            msg = "Command execution error"
            sys.exit(logger.error(msg))
            break
        command = raw_input("\033[4mCommand\033[0m > ")

def fr(exp, url): # File read
    exp(url)
    logger.warning("Please use other tools to exploit this vulnerability. Exit exploit mode")

def fw(exp, url): # File write
    exp(url)

def lfi(exp, url): # Local file include
    exp(url)
    logger.warning("Please use other tools to exploit this vulnerability. Exit exploit mode")

def rfi(exp, url): # Remote file include
    exp(url)
    logger.warning("Please use other tools to exploit this vulnerability. Exit exploit mode")

def sqli(exp, url): # SQL injection
    exp(url)
