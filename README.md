# Scrapy-Amac

![python](https://img.shields.io/badge/Python-3.8.2-green)
![Scrapy](https://img.shields.io/badge/Scrapy-1.6.0-yellow)

## Overview
为方便广大投资者对私募基金信息进行查询，中国基金业协会在官方网站搭建了私募基金分类公示平台，按照私募基金管理人登记的信息对私募基金进行分类公示。
为了全面了解相关机构或者产品信息，学习使用 Scrapy 框架获取部分信息。
+ **[Scrapy](https://github.com/scrapy/scrapy)**  是适用于Python的一个快速、高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试。
Scrapy吸引人的地方在于它是一个框架，任何人都可以根据需求方便的修改。它也提供了多种类型爬虫的基类，如BaseSpider、sitemap爬虫等，最新版本又提供了web2.0爬虫的支持。

+ **[中基协](http://gs.amac.org.cn/)** 中国证券投资基金业协会成立于2012年6月6日，是基金行业相关机构自愿结成的全国性、行业性、非营利性社会组织。
会员包括基金管理公司、基金托管银行、基金销售机构、基金评级机构及其他资产管理机构、相关服务机构。

## Requirements
+ Python 3.5 +
+ Works on Linux, Windows, macOS, BSD


## Install
```
pip install requirements.txt
```
安装过程中如果提示缺少 Twisted, Pywin32 等库，可以在 **[https://www.lfd.uci.edu/](https://www.lfd.uci.edu/~gohlke/pythonlibs/)** 中根据自己 Python 版本下载。

## Run
+ 如果需要获取私募基金管理人

    ![私募基金管理人](https://github.com/bingo-zh/scrapy-amac/blob/master/spider/image/manager.png)
    
    更改 SPIDER_TYPE = 0
    ```
    SPIDER_TYPE = 0
    ```
    在 包含scrapy.cfg 的目录中运行如下命令
    ```
    scrapy crawl manager -o manager.csv
    ```

+ 如果需要获取私募基金

    ![私募基金](https://github.com/bingo-zh/scrapy-amac/blob/master/spider/image/fund.png)
    
    更改 SPIDER_TYPE = 1
    ```
    SPIDER_TYPE = 1
    ```
    在 包含scrapy.cfg 的目录中运行如下命令
    ```
    scrapy crawl fund -o fund.csv
    ```

## Documentation
+ Scrapy 相关文档可参见 **[https://devguide.python.org/](https://devguide.python.org/)**
+ Python 相关文档可参见 **[https://docs.scrapy.org/](https://docs.scrapy.org/)**
## Releases
    仅供学习使用
