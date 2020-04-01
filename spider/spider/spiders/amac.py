# -*- coding: utf-8 -*-
"""
@version: 0.1
@author: zhangwb
中基协私募基金管理人及产品信息爬取
"""
import scrapy
import random
import json
from spider.items import ManagerItem
from spider.items import FundItem
from scrapy.utils.project import get_project_settings


class AmacSpider(scrapy.Spider):

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
        'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/{}/index.html'.format(name),
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }
    r = str(random.uniform(0, 1))
    page = str(0)
    size = str(100)
    post_url_prefix = 'http://gs.amac.org.cn/amac-infodisc/api/pof/{}?rand={}&size={}'.format(name, r, size)
    post_url = post_url_prefix + '&page={}'.format(page)

    # 发起请求
    def start_requests(self):
        yield scrapy.Request(url=self.post_url,
                             method='POST',
                             headers=self.headers,
                             callback=self.parse_list,
                             body="{}")

    # 解析列表
    def parse_list(self, response):
        contents = json.loads(response.body_as_unicode())  # 返回内容json
        content = contents.get('content')
        info_url_prefix = 'http://gs.amac.org.cn/amac-infodisc/res/pof/{}/'.format(self.name)
        # 循环获取info信息
        for i in range(0, len(content)):
            info_url = content[i].get('url')
            yield scrapy.Request(url=info_url_prefix + info_url, headers=self.headers, callback=self.parse_info,
                                 meta={'list_content': content[i]})
        totalpages = contents.get('totalPages')  # 总共多少页
        for i in range(1, totalpages):
            self.page = str(i)
            self.post_url = (self.post_url_prefix + '&page={}').format(self.page)
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
        tbody = response.xpath("//div[@class='info-body']")
        for t in tbody:
            item = ManagerItem()
            item['ID'] = list_content.get('id')# 客户主键

            # 机构诚信信息
            item['CREDITTIPS'] = t.xpath('normalize-space(./div[@class="rule"]//td[contains(text(),"机构诚信信息")]/following-sibling::td)').extract_first()
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


            itemmap = {
                'EN_MANAGERNAME': '基金管理人全称(英文)',  # 基金管理人全称(英文)
                'ORG_CODE': '组织机构代码',  # 组织机构代码
                'ORG_TYPE': '企业性质',  # 企业性质
                'REGISTERPAY': '注册资本(万元)(人民币)',  # 注册资本(万元)(人民币)
                'TUREPAY': '实缴资本(万元)(人民币)',  # 实缴资本(万元)(人民币)
                'PAYRATE': '注册资本实缴比例',  # 注册资本实缴比例
                'BUSINESSTYPE': '业务类型',  # 业务类型
                'STAFF': '员工人数',  # 员工人数
                'ISVIP': '是否为会员',  # 是否为会员
                'VIPTYPE': '当前会员类型',  # 当前会员类型
                'VIPTIME': '入会时间',  # 入会时间
                'LAWSTATUS': '法律意见书状态',  # 法律意见书状态
                'ISTOWORK': '是否有基金从业资格',  # 是否有从业资格
                'WORKWAY': '资格取得方式',  # 资格取得方式
                'LAWORG': '律师事务所名称',  # 律师事务所名称
                'LAWPER': '律师姓名',  # 律师姓名id

            }

            for v in itemmap:
                key = v
                value = itemmap[key]
                item[key] = t.xpath('normalize-space(.//td[contains(text(),"{}")]/following-sibling::td[1]/text())'.format(value)).extract_first()
            return item

    def parse_fund(self, response):
        item = FundItem()
        tbody = response.xpath("//div[@class='info-body']")
        no = response.url
        id_s = self.find_last(no, '/') + 1
        id_e = self.find_last(no, '.')
        no = no[id_s: id_e]
        item['ID'] = no

        itemmap = {
            'FUNDNAME': '基金名称',
            'FUNDID': '基金编号',
            'CHENGLI': '成立时间',
            'BEIAN': '备案时间',
            'BEIAN_JD': '基金备案阶段',
            'FUNDTYPE': '基金类型',
            'BIZHONG': '币种',
            'FUNDMANAGE': '基金管理人名称',
            'MANAGETYPE': '管理类型',
            'TUOGUANMANAGE': '托管人名称',
            'STATUS': '运作状态',
            'LASTUPDATETIME': '基金信息最后更新时间',
            'REMARK': '特别提示',
            'HALFY_R': '半年报',
            'YEAR_R': '年报',
            'QUARTER_R': '季报',
            'MONTH_R': '当月月报',
        }

        for v in itemmap:
            key = v
            value = itemmap[key]
            vv = ''
            if key == 'FUNDNAME':

                vv = tbody.xpath('normalize-space(.//td[contains(text(),"{}")]/following-sibling::td[1]/text())'.format(
                    value)).extract_first()
            else:
                vv = tbody.xpath('string(.//td[contains(text(),"{}")]/following-sibling::td)'.format(
                    value)).extract_first()

            vv = vv.replace('，', ';')
            item[key] = vv

        glr_bh = tbody.xpath('normalize-space(.//td[contains(text(),"{}")]/following-sibling::td[1]/a/@href)'.format(
                "基金管理人名称")).extract_first()

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
