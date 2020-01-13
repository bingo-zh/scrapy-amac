# -*- coding: utf-8 -*-
import scrapy
import random
import json
from spider.items import ManagerItem
from spider.items import FundItem
from scrapy.utils.project import get_project_settings


class AmacSpider(scrapy.Spider):
    #scrapy crawl myspider -a category=electronicstbody
    # def __init__(self, category=None, *args, **kwargs):
    #     super(MySpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ['http://www.example.com/categories/%s' % category]
    #

    settings = get_project_settings()
    spidertype = settings.get('SPIDER_TYPE')
    if spidertype == 0:
        name = 'manager'
    elif spidertype == 1:
        name = 'fund'
    allowed_domains = ['gs.amac.org.cn']
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json',
        'Host': 'gs.amac.org.cn',
        'Origin': 'http://gs.amac.org.cn',
        'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/'+name+'/index.html',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }
    r = str(random.uniform(0, 1))
    page = str(0)
    size = str(100)
    post_url_prefix = 'http://gs.amac.org.cn/amac-infodisc/api/pof/'+name+'?rand=' + r + '&size=' + size
    post_url = post_url_prefix + '&page=' + page

    def start_requests(self):
        yield scrapy.Request(url=self.post_url,
                             method='POST',
                             headers=self.headers,
                             callback=self.parse_list,
                             body="{}")

    def parse_list(self, response):
        contents = json.loads(response.body_as_unicode())  # 返回内容json
        content = contents.get('content')
        info_url_prefix = 'http://gs.amac.org.cn/amac-infodisc/res/pof/'+self.name+'/'
        # 循环获取info信息
        for i in range(0, len(content)):
            info_url = content[i].get('url')
            yield scrapy.Request(url=info_url_prefix + info_url, headers=self.headers, callback=self.parse_info,
                                 meta={'list_content': content[i]})
        totalpages = contents.get('totalPages')  # 总共多少页
        for i in range(1, totalpages):
            self.page = str(i)
            self.post_url = self.post_url_prefix + '&page=' + self.page
            yield scrapy.Request(url=self.post_url,
                                 method='POST',
                                 headers=self.headers,
                                 callback=self.parse_list,
                                 body="{}")

    def parse_info(self, response):
        if self.spidertype == 0:
            yield self.parse_manager(response)
        elif self.spidertype == 1:
            yield self.parse_fund(response)

    def parse_manager(self, response):
        list_content = response.meta['list_content']
        u = response.url
        tbody = response.xpath("//table[contains(@class , 'table') "
                               "and contains(@class, 'table-center') "
                               "and contains(@class, 'table-info')]/tbody")
        for t in tbody:
            item = ManagerItem()

            item['ID'] = list_content.get('id')# 客户主键
            item['MANAGERNAME'] = list_content.get('managerName') # 基金管理人全称(中文)
            item['ARTIFICIALPERSONNAME'] = list_content.get('artificialPersonName')# 法定代表人/执行事务合伙人(委派代表)姓名
            item['REGISTERNO'] = list_content.get('registerNo') # 登记编号
            item['ESTABLISHDATE'] = list_content.get('establishDate')# 成立时间
            item['MANAGERHASPRODUCT'] = list_content.get('managerHasProduct')#
            item['URL'] = u#
            item['REGISTERDATE'] = list_content.get('registerDate') # 登记时间
            item['REGISTERADDRESS'] = list_content.get('registerAddress') # 注册地址
            item['REGISTERPROVINCE'] = list_content.get('registerProvince') # 注册省份
            item['REGISTERCITY'] = list_content.get('registerCity') # 注册城市
            item['REGADRAGG'] = list_content.get('regAdrAgg') # 注册地区
            item['FUNDCOUNT'] = list_content.get('fundCount') # 基金数量
            item['FUNDSCALE'] = list_content.get('fundScale')# 基金规模
            item['PAIDINCAPITAL'] = list_content.get('paidInCapital')#
            item['SUBSCRIBEDCAPITAL'] = list_content.get('subscribedCapital') #
            item['HASSPECIALTIPS'] = list_content.get('hasSpecialTips') # 特别提示
            item['INBLACKLIST'] = list_content.get('inBlacklist') # 黑名单
            item['HASCREDITTIPS'] = list_content.get('hasCreditTips') # 机构诚信信息
            item['REGCOORDINATE'] = list_content.get('regCoordinate') # 注册坐标
            item['OFFICECOORDINATE'] = list_content.get('officeCoordinate') # 办公坐标
            item['OFFICEADDRESS'] = list_content.get('officeAddress') # 办公地址
            item['OFFICEPROVINCE'] = list_content.get('officeProvince')# 办公省份
            item['OFFICECITY'] = list_content.get('officeCity')# 办公城市
            item['PRIMARYINVESTTYPE'] = list_content.get('primaryInvestType') # 机构类型
            item['EN_MANAGERNAME'] = t.xpath('normalize-space(.//td[contains(text(),"基金管理人全称(英文)")]/following-sibling::td[1]/text())').extract_first() # 基金管理人全称(英文)
            item['ORG_CODE'] = t.xpath('normalize-space(.//td[contains(text(),"组织机构代码")]/following-sibling::td[1]/text())').extract_first() # 组织机构代码
            item['ORG_TYPE'] = t.xpath('normalize-space(.//td[contains(text(),"企业性质")]/following-sibling::td[1]/text())').extract_first() # 企业性质

            # 诚信信息
            ccxx_tr = []
            ccxx_tr_td = t.xpath('./tr[1]/td[@class="td-content"]/table/tr')
            for td in ccxx_tr_td:
                tx = td.xpath('normalize-space(string(.//td))').extract()
                ccxx_tr.append(":".join(tx))

            item['CREDITTIPS'] = '机构诚信信息==>' + ';'.join(ccxx_tr)  # 机构诚信信息
            item['REGISTERPAY'] = t.xpath('normalize-space(.//td[contains(text(),"注册资本(万元)(人民币)")]/following-sibling::td[1]/text())').extract_first() # 注册资本(万元)(人民币)
            item['TUREPAY'] = t.xpath('normalize-space(.//td[contains(text(),"实缴资本(万元)(人民币)")]/following-sibling::td[1]/text())').extract_first() # 实缴资本(万元)(人民币)
            item['PAYRATE'] = t.xpath('normalize-space(.//td[contains(text(),"注册资本实缴比例")]/following-sibling::td[1]/text())').extract_first() # 注册资本实缴比例
            item['BUSINESSTYPE'] = t.xpath('normalize-space(.//td[contains(text(),"业务类型")]/following-sibling::td[1]/text())').extract_first() # 业务类型
            item['STAFF'] = t.xpath('normalize-space(.//td[contains(text(),"员工人数")]/following-sibling::td[1]/text())').extract_first() # 员工人数
            item['ISVIP'] = t.xpath('normalize-space(.//td[contains(text(),"是否为会员")]/following-sibling::td[1]/text())').extract_first() # 是否为会员
            item['VIPTYPE'] = t.xpath('normalize-space(.//td[contains(text(),"当前会员类型")]/following-sibling::td[1]/text())').extract_first() # 当前会员类型
            item['VIPTIME'] = t.xpath('normalize-space(.//td[contains(text(),"入会时间")]/following-sibling::td[1]/text())').extract_first()# 入会时间
            item['LAWSTATUS'] = t.xpath('normalize-space(.//td[contains(text(),"法律意见书状态")]/following-sibling::td[1]/text())').extract_first() # 法律意见书状态
            item['ISTOWORK'] = t.xpath('normalize-space(.//td[contains(text(),"是否有基金从业资格")]/following-sibling::td[1]/text())').extract_first() # 是否有从业资格
            item['WORKWAY'] = t.xpath('normalize-space(.//td[contains(text(),"资格取得方式")]/following-sibling::td[1]/text())').extract_first() # 资格取得方式
            item['LAWORG'] = t.xpath('normalize-space(.//td[contains(text(),"律师事务所名称")]/following-sibling::td[1]/text())').extract_first() # 律师事务所名称
            item['LAWPER'] = t.xpath('normalize-space(.//td[contains(text(),"律师姓名")]/following-sibling::td[1]/text())').extract_first() # 律师姓名id
            return item

    def parse_fund(self, response):
        item = FundItem()
        tbody = response.xpath("//table[contains(@class , 'table') and contains(@class, 'table-center') "
                               "and contains(@class, 'table-info')]/tbody")
        no = response.url
        id_s = self.find_last(no, '/') + 1
        id_e = self.find_last(no, '.')
        no = no[id_s: id_e]
        item['ID'] = no
        item['FUNDNAME'] = tbody.xpath('./tr[1]/td[@class="td-content"]/text()').extract_first()
        item['FUNDID'] = tbody.xpath('./tr[2]/td[@class="td-content"]/text()').extract_first()
        item['CHENGLI'] = tbody.xpath('./tr[3]/td[@class="td-content"]/text()').extract_first()
        item['BEIAN'] = tbody.xpath('./tr[4]/td[@class="td-content"]/text()').extract_first()
        item['BEIAN_JD'] = tbody.xpath('./tr[5]/td[@class="td-content"]/text()').extract_first()
        item['FUNDTYPE'] = tbody.xpath('./tr[6]/td[@class="td-content"]/text()').extract_first()
        item['BIZHONG'] = tbody.xpath('./tr[7]/td[@class="td-content"]/text()').extract_first()
        item['FUNDMANAGE'] = tbody.xpath('./tr[8]/td[@class="td-content"]/a/text()').extract_first()
        item['MANAGETYPE'] = tbody.xpath('./tr[9]/td[@class="td-content"]/text()').extract_first()
        item['TUOGUANMANAGE'] = tbody.xpath('./tr[10]/td[@class="td-content"]/text()').extract_first()
        item['STATUS'] = tbody.xpath('./tr[11]/td[@class="td-content"]/text()').extract_first()
        item['LASTUPDATETIME'] = tbody.xpath('./tr[12]/td[@class="td-content"]/text()').extract_first()
        item['REMARK'] = tbody.xpath('./tr[13]/td[@class="td-content"]/text()').extract_first()
        item['MONTH_R'] = tbody.xpath('./tr[15]/td[@class="td-content"]/text()').extract_first()
        item['HALFY_R'] = tbody.xpath('./tr[16]/td[@class="td-content"]/text()').extract_first()
        item['YEAR_R'] = tbody.xpath('./tr[17]/td[@class="td-content"]/text()').extract_first()
        item['QUARTER_R'] = tbody.xpath('./tr[18]/td[@class="td-content"]/text()').extract_first()
        glr_bh = tbody.xpath('./tr[8]/td[@class="td-content"]/a/@href').extract_first()
        glr_bh_s = self.find_last(glr_bh, '/') + 1
        glr_bh_e = self.find_last(glr_bh, '.')
        glr_bh = glr_bh[glr_bh_s: glr_bh_e]
        item['PARENTID'] = glr_bh
        return item

    # 获取最后出现的位置
    def find_last(self, s1, s2):
        last_position = -1
        while True:
            position = s1.find(s2, last_position + 1)
            if position == -1:
                return last_position
            last_position = position