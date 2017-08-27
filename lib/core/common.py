#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import sys
import imp
import time
import logging
from lib.core.data import *
from lib.core.exception import *
from lib.utils.expfunctions import *
from lib.core.log import LOGGER_HANDLER
from lib.core.settings import BANNER, UNICODE_ENCODING, NULL, INVALID_UNICODE_CHAR_FORMAT, OPTIONAL_MOUDLE_METHODS
from lib.core.convert import stdoutencode
from lib.core.enums import EXIT_STATUS, TARGET_MODE_STATUS
from thirdparty.termcolor.termcolor import colored
from thirdparty.odict.odict import OrderedDict
from thirdparty.prettytable.prettytable import PrettyTable


def setPaths():#设置POC-T的文件路径和目录
    """
    设置Sepia的绝对路径
    """
    root_path = paths.ROOT_PATH
    paths.DATA_PATH = os.path.join(root_path, "data") #设置data文件夹路径
    paths.SCRIPT_PATH = os.path.join(root_path, "script") #设置script文件夹路径
    paths.CONFIG_PATH = os.path.join(root_path, "toolkit.conf") #设置toolkit.conf文件路径
    #如果data、script、output三个文件夹都不存在就创建
    if not os.path.exists(paths.SCRIPT_PATH):
        os.mkdir(paths.SCRIPT_PATH)
    if not os.path.exists(paths.DATA_PATH):
        os.mkdir(paths.DATA_PATH)

    paths.WEAK_PASS = os.path.join(paths.DATA_PATH, "pass100.txt") #设置弱口令文件pass100.txt的路径
    paths.LARGE_WEAK_PASS = os.path.join(paths.DATA_PATH, "pass1000.txt") #设置弱口令文件pass1000.txt的路径
    paths.UA_LIST_PATH = os.path.join(paths.DATA_PATH, "user-agents.txt") #设置user-agents.txt文件的路径

    if os.path.isfile(paths.CONFIG_PATH) and os.path.isfile(paths.WEAK_PASS) and os.path.isfile(
            paths.LARGE_WEAK_PASS) and os.path.isfile(paths.UA_LIST_PATH):
        pass
    else:
        #如果toolkit.conf、pass100.txt、pass1000.txt、user-agent.txt四个缺失任何一个，就抛出异常
        msg = 'Some files missing, it may cause an issue.'
        raise ToolkitMissingPrivileges(msg)

def checkFile(filename):
    """
    function Checks for file existence and readability
    """
    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except IOError:
            valid = False

    if not valid:
        raise ToolkitSystemException("unable to read file '%s'" % filename)


def banner():
    """
    Function prints banner with its version
    """
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    dataToStdout(_)


def dataToStdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """
    logging._acquireLock()
    if isinstance(data, unicode):
        message = stdoutencode(data)
    else:
        message = data

    sys.stdout.write(setColor(message, bold))

    try:
        sys.stdout.flush()
    except IOError:
        pass

    logging._releaseLock()
    return


def setColor(message, bold=False):
    retVal = message

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            retVal = colored(message, color=None, on_color=None, attrs=("bold",))

    return retVal


def pollProcess(process, suppress_errors=False):
    """
    Checks for process status (prints > if still running)
    """

    while True:
        message = '>'
        sys.stdout.write(message)
        try:
            sys.stdout.flush()
        except IOError:
            pass

        time.sleep(1)

        returncode = process.poll()

        if returncode is not None:
            if not suppress_errors:
                if returncode == 0:
                    print " done\n"
                elif returncode < 0:
                    print " process terminated by signal %d\n" % returncode
                elif returncode > 0:
                    print " quit unexpectedly with return code %d\n" % returncode
            break


def getSafeExString(ex, encoding=None):
    """
    Safe way how to get the proper exception represtation as a string
    (Note: errors to be avoided: 1) "%s" % Exception(u'\u0161') and 2) "%s" % str(Exception(u'\u0161'))
    """
    retVal = ex

    if getattr(ex, "message", None):
        retVal = ex.message
    elif getattr(ex, "msg", None):
        retVal = ex.msg

    return getUnicode(retVal, encoding=encoding)


def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return NULL

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except Exception:
                    value = value[:ex.start] + "".join(
                        INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))


def systemQuit(status=EXIT_STATUS.SYSETM_EXIT):
    if status == EXIT_STATUS.USER_QUIT and "is_continue" not in th:
        logger.info('User quit')
        logger.error('System exit')
    elif status == EXIT_STATUS.USER_QUIT and "exploit_mode" in th:
        if th.exploit_mode:
            logger.error('Exit exploit mode')
            logger.info('System exit')
    else:
        if status == EXIT_STATUS.SYSETM_EXIT:
            printResult()
            if conf.TARGET_MODE == TARGET_MODE_STATUS.SINGLE: #如果是扫描单个目标就启动attack
                attack()
            logger.info('System exit')
        elif status == EXIT_STATUS.USER_QUIT and th.is_continue:
            dataToStdout('\n')
            printResult()
            logger.info('User quit')
            logger.error('System exit')
        elif status == EXIT_STATUS.ERROR_EXIT and th.is_continue:
            dataToStdout('\n')
            printResult()
            logger.error('System exit')
        else:
            raise ToolkitValueException('Invalid status code: %s' % str(status))
    sys.exit(0)

def printResult():
    targetsheet = PrettyTable(["Target", "Vulnerable"])
    targetsheet.align["Target"] = "l"
    targetsheet.padding_width = 1
    for i in targetlist:
        targetsheet.add_row(i)
    print targetsheet
    msg = '{} found | {} scanned in {} second'.format(th.found_count, th.scan_count, str(time.time()-th.start_time)[0:4])
    out = '{}\n'.format(msg)
    dataToStdout(out)

def attack():
    if len(targetlist) and targetlist[0][1]:
        for each in OPTIONAL_MOUDLE_METHODS: #OPTIONAL_MOUDLE_METHODS=['exp']
            if not hasattr(th.module_obj, each): #如果模块中不存在'exp'方法就提醒并退出
                msg = "The script does not contain any exploit module"
                logger.warning(msg)
                sys.exit(logger.info('System exit'))
            else:
                try:
                    expfunc = th.module_obj._type.lower() #加载攻击模块
                    msg = "Enter exploit mode"
                    logger.info(msg)
                    th.exploit_mode = True
                    eval(expfunc)(th.module_obj.exp, conf.SINGLE_TARGET_STR)
                except AttributeError:
                    logger.warning("The script does not specify an attack type.Exited the attack mode")
                    sys.exit(logger.info('System exit'))
                

def getFileItems(filename, commentPrefix='#', unicode_=True, lowercase=False, unique=False):
    """
    @function returns newline delimited items contained inside file
    """

    retVal = list() if not unique else OrderedDict()

    checkFile(filename)

    try:
        with open(filename, 'r') as f:
            for line in (f.readlines() if unicode_ else f.xreadlines()):
                # xreadlines doesn't return unicode strings when codecs.open() is used
                if commentPrefix and line.find(commentPrefix) != -1:
                    line = line[:line.find(commentPrefix)]

                line = line.strip()

                if not unicode_:
                    try:
                        line = str.encode(line)
                    except UnicodeDecodeError:
                        continue

                if line:
                    if lowercase:
                        line = line.lower()

                    if unique and line in retVal:
                        continue

                    if unique:
                        retVal[line] = True

                    else:
                        retVal.append(line)

    except (IOError, OSError, MemoryError), ex:
        errMsg = "something went wrong while trying "
        errMsg += "to read the content of file '%s' ('%s')" % (filename, ex)
        raise ToolkitSystemException(errMsg)

    return retVal if not unique else retVal.keys()
