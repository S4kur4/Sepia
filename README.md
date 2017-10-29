# Sepia-乌贼
[![Python 2.7](https://img.shields.io/badge/python-2.7-red.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-blue.svg)](https://github.com/S4kur4/Sepia/blob/master/LICENSE)

Sepia(乌贼)是一款集PoC批量验证和漏洞攻击的渗透测试工具，能满足漏洞爆发时快速对资产状况进行查证的需求。

<img src="https://i.loli.net/2017/08/27/59a268fc4eccb.png" width="600" height="424">

## 一些说明
Sepia是在POC-T的基础上做了精简、改进而成的，因此首先要感谢@cdxy的POC-T项目：[POC-T](https://github.com/Xyntax/POC-T)。

与POC-T相比，Sepia有以下一些变化：

**1. 数据搜集方式的变化**

去掉了Google dork、Shodan dork，只保留了Zoomeye dork，增加了Baidu dork(URL爬虫)。

**2. 增加了URL正则抓取定制功能**

一些Web应用程序的漏洞其对应的URL可能千变万化，仅利用@cdxy批量[规范URL的方法](https://www.cdxy.me/?p=640)会降低验证效率，因此Sepia在toolkit文件中增加了正则定制项`urlfilter`，通过配合百度URL爬虫，能大大提升抓取和验证的效率。

**3. 改变了一些输出显示**

Sepia去掉了POC-T导出到文件的功能，引入`prettytable`直接将结果做成表格显示在终端。

**4. 脚本编写要求的变化**

由于Sepia含有漏洞的攻击功能，但各种漏洞的攻击方式会有很大差异，目前已经基本确定了Sepia的脚本编写规则和标准，这应该是和POC-T有比较大区别的地方。

**总之，POC-T专注的是并发批量处理任务，而Sepia只专注高效批量PoC验证并能对单个目标实施攻击。**

## Wiki

* [参数说明](https://github.com/S4kur4/Sepia/wiki/参数说明)
* [使用举例](https://github.com/S4kur4/Sepia/wiki/使用举例)

## 后话

Sepia还处于开发版本阶段，有任何问题烦请发邮件至：[s4kur4s4kur4@gmail.com](mailto:s4kur4s4kur4@gmail.com?Subject=Hello%20S4kur4)。
2017年10月29日更新：由于ZoomEye方面一直处于升级更新状态，近期本来想完善Sepia的ZoomEye Dork代码，但ZoomEye的API迟迟未开放导致不能继续完善。暂时我先慢慢完扩充脚本库吧。

