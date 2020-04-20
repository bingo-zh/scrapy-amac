# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'
IS_RANDOM_UA = 1  # 随机User-Agent
SPIDER_TYPE = 0  # 0:管理人(manager),1:产品(fund)

ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
#DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'spider.middlewares.SpiderSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'spider.middlewares.UADownloaderMiddleware': 541,
   'spider.middlewares.SpiderDownloaderMiddleware': 542,
   'spider.middlewares.RetryRecordMiddleware': 543,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'spider.pipelines.SpiderPipeline': 300,
#    # 'spider.pipelines.OraclePipline': 544,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
FEED_EXPORT_ENCODING = "utf-8-sig"
# FEED_EXPORTERS = {
#    'csv': 'spider.spiders.AmacItemExporter.AmacItemExporter',
# }
# FIELDS_TO_EXPORT = [
#    'ID',  # 编号
#    'FUNDNAME',  # 基金名称
#    'FUNDID',  # 基金编号
#    'CHENGLI',  # 成立时间
#    'BEIAN',  # 备案时间
#    'BEIAN_JD',  # 备案阶段
#    'FUNDTYPE',  # 基金类型
#    'BIZHONG',  # 币种
#    'FUNDMANAGE',  # 基金管理人名称
#    'MANAGETYPE',  # 管理类型
#    'TUOGUANMANAGE',  # 托管人名称
#    'STATUS',  # 运作状态
#    'LASTUPDATETIME',  # 最后更新时间
#    'REMARK',  # 特别提醒
#    'MONTH_R',  # 月报
#    'HALFY_R',  # 半年报
#    'YEAR_R',  # 年报
#    'QUARTER_R',  # 季报
#    'PARENTID'
# ]
#
FIELDS_TO_EXPORT = [
   'ID',#客户主键
   'MANAGERNAME',#基金管理人全称(中文)
   'ARTIFICIALPERSONNAME',#法定代表人/执行事务合伙人(委派代表)姓名
   'REGISTERNO',#登记编号
   'ESTABLISHDATE',#成立时间
   'MANAGERHASPRODUCT',#
   'URL',#
   'REGISTERDATE',#登记时间
   'REGISTERADDRESS',#注册地址
   'REGISTERPROVINCE',#注册省份
   'REGISTERCITY',#注册城市
   'REGADRAGG',#注册地区
   'FUNDCOUNT',#基金数量
   'FUNDSCALE',#基金规模
   'PAIDINCAPITAL',#
   'SUBSCRIBEDCAPITAL',#
   'HASSPECIALTIPS',#特别提示
   'INBLACKLIST',#黑名单
   'HASCREDITTIPS',#机构诚信信息
   'REGCOORDINATE',#注册坐标
   'OFFICECOORDINATE',#办公坐标
   'OFFICEADDRESS',#办公地址
   'OFFICEPROVINCE',#办公省份
   'OFFICECITY',#办公城市
   'PRIMARYINVESTTYPE',#机构类型
   'EN_MANAGERNAME',#基金管理人全称(英文)
   'ORG_CODE',#组织机构代码
   'ORG_TYPE',#企业性质
   'CREDITTIPS',#机构诚信信息
   'REGISTERPAY',#注册资本(万元)(人民币)
   'TUREPAY',#实缴资本(万元)(人民币)
   'PAYRATE',#注册资本实缴比例
   'BUSINESSTYPE',#注册资本实缴比例
   'STAFF',#员工人数
   'ISVIP',#是否为会员
   'VIPTYPE',#当前会员类型
   'VIPTIME',#入会时间
   'LAWSTATUS',#法律意见书状态
   'ISTOWORK',#是否有从业资格
   'WORKWAY',#资格取得方式
   'LAWORG',#律师事务所名称
   'LAWPER',#律师姓名
]
