#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path
import traceback
from lib.parse.cmdline import cmdLineParser #导入命令行解析模块
from lib.core.option import initOptions
from lib.controller.loader import loadModule, loadPayloads #导入脚本加载模块
from lib.core.common import setPaths, banner, systemQuit
from lib.core.data import paths, logger, cmdLineOptions
from lib.core.enums import EXIT_STATUS
from lib.core.settings import IS_WIN #判断是否为Windows
from lib.core.exception import ToolkitUserQuitException
from lib.core.exception import ToolkitMissingPrivileges
from lib.core.exception import ToolkitSystemException
from lib.controller.engine import run
from thirdparty.colorama.initialise import init as winowsColorInit #导入第三方插件Colorama


def main():
    try:
        paths.ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        #得到当前py文件所在文件夹上一个文件夹目录赋值给paths.ROOT_PATH，也就是Sepia的根目录
        try:
            os.path.isdir(paths.ROOT_PATH) #此处判断path.ROOT_PATH得到的路径编码是否正常
        except UnicodeEncodeError: #出现编码错误就退出
            errMsg = "Your system does not properly handle non-ASCII paths. "
            errMsg += "Please move the project root directory to another location"
            logger.error(errMsg)
            raise SystemExit
        setPaths() #设置Sepia的文件路径和目录
        banner() #打印Sepia的logo
        '''
        print "########以下为paths字典#########"
        print paths
        '''
        #存储原始命令行选项，以备恢复
        '''
        print "########以下为原始命令行参数#########"
        print cmdLineParser().__dict__
        '''
        #cmdLineParser().__dict__获得命令行参数数据字典并赋值给cmdLineOptions字典对象
        cmdLineOptions.update(cmdLineParser().__dict__)
        initOptions(cmdLineOptions)
        '''
        print "########以下为cmdLineOption字典#########"
        print cmdLineOptions
        '''
        
        if IS_WIN: #如果是Windows使用Colorama插件并初始化
            winowsColorInit()
        

        loadModule() #加载poc脚本
        loadPayloads() #配置扫描模式

        run() #开始扫描

        systemQuit(EXIT_STATUS.SYSETM_EXIT)

    except ToolkitMissingPrivileges, e:
        logger.error(e)
        systemQuit(EXIT_STATUS.ERROR_EXIT)

    except ToolkitSystemException, e:
        logger.error(e)
        systemQuit(EXIT_STATUS.ERROR_EXIT)

    except ToolkitUserQuitException:
        systemQuit(EXIT_STATUS.USER_QUIT)
    except KeyboardInterrupt:
        systemQuit(EXIT_STATUS.USER_QUIT)

    except Exception:
        print traceback.format_exc()
        logger.warning('It seems like you reached a unhandled exception, please report it to :s4kur4s4kur4@gmail.com')

if __name__ == "__main__":
    main()
