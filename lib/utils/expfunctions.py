#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from lib.core.data import logger

def rce(exp, url):
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