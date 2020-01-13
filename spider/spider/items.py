# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundItem(scrapy.Item):
    BEIAN = scrapy.Field()
    BEIAN_JD = scrapy.Field()
    BIZHONG = scrapy.Field()
    CHENGLI = scrapy.Field()
    FUNDID = scrapy.Field()
    FUNDMANAGE = scrapy.Field()
    FUNDNAME = scrapy.Field()
    FUNDTYPE = scrapy.Field()
    HALFY_R = scrapy.Field()
    ID = scrapy.Field()
    LASTUPDATETIME = scrapy.Field()
    MANAGETYPE = scrapy.Field()
    MONTH_R = scrapy.Field()
    PARENTID = scrapy.Field()
    QUARTER_R = scrapy.Field()
    REMARK = scrapy.Field()
    STATUS = scrapy.Field()
    TUOGUANMANAGE = scrapy.Field()
    YEAR_R = scrapy.Field()


class ManagerItem(scrapy.Item):
    ID = scrapy.Field()
    MANAGERNAME = scrapy.Field()
    ARTIFICIALPERSONNAME = scrapy.Field()
    REGISTERNO = scrapy.Field()
    ESTABLISHDATE = scrapy.Field()
    MANAGERHASPRODUCT = scrapy.Field()
    URL = scrapy.Field()
    REGISTERDATE = scrapy.Field()
    REGISTERADDRESS = scrapy.Field()
    REGISTERPROVINCE = scrapy.Field()
    REGISTERCITY = scrapy.Field()
    REGADRAGG = scrapy.Field()
    FUNDCOUNT = scrapy.Field()
    FUNDSCALE = scrapy.Field()
    PAIDINCAPITAL = scrapy.Field()
    SUBSCRIBEDCAPITAL = scrapy.Field()
    HASSPECIALTIPS = scrapy.Field()
    INBLACKLIST = scrapy.Field()
    HASCREDITTIPS = scrapy.Field()
    REGCOORDINATE = scrapy.Field()
    OFFICECOORDINATE = scrapy.Field()
    OFFICEADDRESS = scrapy.Field()
    OFFICEPROVINCE = scrapy.Field()
    OFFICECITY = scrapy.Field()
    PRIMARYINVESTTYPE = scrapy.Field()
    EN_MANAGERNAME = scrapy.Field()
    ORG_CODE = scrapy.Field()
    ORG_TYPE = scrapy.Field()
    CREDITTIPS = scrapy.Field()
    REGISTERPAY = scrapy.Field()
    TUREPAY = scrapy.Field()
    PAYRATE = scrapy.Field()
    BUSINESSTYPE = scrapy.Field()
    STAFF = scrapy.Field()
    ISVIP = scrapy.Field()
    VIPTYPE = scrapy.Field()
    VIPTIME = scrapy.Field()
    LAWSTATUS = scrapy.Field()
    ISTOWORK = scrapy.Field()
    WORKWAY = scrapy.Field()
    LAWORG = scrapy.Field()
    LAWPER = scrapy.Field()

