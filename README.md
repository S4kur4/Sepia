# Sepia
Sepia(乌贼)是一款集PoC批量验证和攻击的内部安全团队工具，能满足内部团队在漏洞爆发时快速对资产状况进行查证的需求。

![Sepia.png](https://i.loli.net/2017/08/25/599fad297f88e.png)

## 一些说明
Sepia是在POC-T的基础上做了精简修改而成的，因此首先要感谢@cdxy的POC-T项目：<https://github.com/Xyntax/POC-T>。与POC-T相比，Sepia有以下一些变化：

+ #####数据搜集方式的变化

去掉了Google dork、Shodan dork，只保留了Zoomeye dork，增加了Baidu URL爬虫。

+  ##### 增加了URL正则抓取定制功能

由于每一个漏洞对应的URL可能千变万化，仅利用@cdxy批量[规范URL的方法](https://www.cdxy.me/?p=640)会降低验证效率，因此Sepia在toolkit文件中增加了正则定制项`urlfilter`，通过配合百度URL爬虫，能大大提升抓取和验证的效率。

+ #####改变了一些输出显示

Sepia去掉了POC-T导出到文件的功能，引入`prettytable`直接将结果做成表格显示在终端。

+ #####脚本编写要求的变化

由于Sepia含有漏洞的攻击功能，但各种漏洞的攻击方式会有很大差异，因此考虑定制一些标准将攻击功能直接交给脚本来做，目前仍在构思这部分，这应该是和POC-T有比较大区别的地方。

**总之，POC-T专注的是并发批量处理任务，而Sepia只专注高效批量PoC验证并能实施攻击。**

## 脚本

脚本这一块目前仍然依赖于POC-T的脚本库，由于后期Sepia会从脚本层面增加攻击功能，等Sepia制定完善了脚本编写文档后会逐渐丰富自己的脚本库。

## 后话

Sepia还处于开发版本阶段，有任何问题烦请发邮件至[s4kur4s4kur4@gmail.com](mailto:s4kur4s4kur4@gmail.com?Subject=Hello%20S4kur4)。

