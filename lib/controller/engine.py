#!/usr/bin/env python
#-*- coding:utf-8 -*-


import threading
import time
import traceback
from lib.core.data import th, conf, logger, targetlist
from lib.utils.console import getTerminalSize #获取命令行窗口的宽度和高度
from lib.utils.versioncheck import PYVERSION
from lib.core.enums import POC_RESULT_STATUS, ENGINE_MODE_STATUS


def initEngine():
    th.thread_mode = True if conf.ENGINE is ENGINE_MODE_STATUS.THREAD else False
    #多线程模式conf.ENGINE=9
    th.module_name = conf.MODULE_NAME #脚本名
    th.s_flag = True
    th.thread_count = th.threads_num = th.THREADS_NUM #线程数
    th.scan_count = th.found_count = 0 #扫描数和发现数置0
    th.console_width = getTerminalSize()[0] - 2 #命令行窗口宽度减2
    th.is_continue = True
    th.start_time = time.time() #开始计时
    setThreadLock()
    '''
    print "#########以下是th字典##########"
    print th
    '''
    msg = 'The number of %s: %d' % ('threads' if conf.ENGINE is ENGINE_MODE_STATUS.THREAD else 'concurrent', th.threads_num)
    logger.info(msg)


def scan():
    while 1:
        if th.thread_mode: th.load_lock.acquire()
        if th.queue.qsize() > 0 and th.is_continue:
            payload = str(th.queue.get(timeout=1.0))
            if th.thread_mode: th.load_lock.release()
        else:
            if th.thread_mode: th.load_lock.release()
            break
        try:
            #POC在执行时报错如果不被处理，线程框架会停止并退出
            status = th.module_obj.poc(payload) #执行脚本，会返回状态True或者False
            resultHandler(status, payload)
        except Exception:
            th.errmsg = traceback.format_exc()
            th.is_continue = False
        changeScanCount(1)
    changeThreadCount(-1)


def run():
    initEngine()
    if conf.ENGINE is ENGINE_MODE_STATUS.THREAD: #多线程模式conf.ENGINE=9
        for i in range(th.threads_num):
            t = threading.Thread(target=scan, name=str(i))
            setThreadDaemon(t)
            t.start()
        # It can quit with Ctrl-C
        while 1: #如果未扫描结束，主线程一直死循环等待，取决于线程数量和th.is_continue的值
            if th.thread_count > 0 and th.is_continue:
                time.sleep(0.01)
            else:
                break

    elif conf.ENGINE is ENGINE_MODE_STATUS.GEVENT: #协程模式conf.ENGINE=8
        from gevent import monkey
        monkey.patch_all()
        import gevent
        while th.queue.qsize() > 0 and th.is_continue:
            gevent.joinall([gevent.spawn(scan) for i in xrange(0, th.threads_num) if #生成10个concurrent
                            th.queue.qsize() > 0])

    if 'errmsg' in th:
        logger.error(th.errmsg)


def resultHandler(status, payload):
    truemsg = "The target '{}' is vulnerable".format(payload)
    falsemsg = "The target '{}' is NOT vulnerable".format(payload)
    if not status or status is POC_RESULT_STATUS.FAIL:
        targetlist.append([payload, status])
        logger.error(falsemsg)
        return
    elif status is POC_RESULT_STATUS.RETRAY:
        changeScanCount(-1)
        th.queue.put(payload)
        return
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        targetlist.append([payload, status])
        logger.success(truemsg)
        changeFoundCount(1)
    else:
        pass
    


def setThreadLock():
    if th.thread_mode:
        th.found_count_lock = threading.Lock()
        th.scan_count_lock = threading.Lock()
        th.thread_count_lock = threading.Lock()
        th.file_lock = threading.Lock()
        th.load_lock = threading.Lock()


def setThreadDaemon(thread): #设置守护线程
    # Reference: http://stackoverflow.com/questions/190010/daemon-threads-explanation
    if PYVERSION >= "2.6":
        thread.daemon = True
    else:
        thread.setDaemon(True)


def changeFoundCount(num):
    if th.thread_mode: th.found_count_lock.acquire()
    th.found_count += num
    if th.thread_mode: th.found_count_lock.release()


def changeScanCount(num):
    if th.thread_mode: th.scan_count_lock.acquire()
    th.scan_count += num
    if th.thread_mode: th.scan_count_lock.release()


def changeThreadCount(num):
    if th.thread_mode: th.thread_count_lock.acquire()
    th.thread_count += num
    if th.thread_mode: th.thread_count_lock.release()
