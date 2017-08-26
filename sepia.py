#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Sepia是在POC-T的基础上修改并改进的一款集PoC验证和漏洞攻击的内部安全团队工具
感谢POC-T项目：https://github.com/Xyntax/POC-T
感谢原作者@cdxy：https://www.cdxy.me
'''
import sys
sys.dont_write_bytecode = True

from lib.utils import versioncheck  # 进行版本检查
from lib.cli import main #导入主函数模块

if __name__ == '__main__':
    main()