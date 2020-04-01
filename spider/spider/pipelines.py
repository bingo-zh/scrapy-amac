# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
import cx_Oracle

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class OraclePipline(object):

    def open_spider(self, spider):
        self.conn = self.getconn()
        self.cursor = self.conn.cursor()
        self.settings = get_project_settings()
        self.spidertype = self.settings.get('SPIDER_TYPE')
        if self.spidertype == 1:
            table = 't_amac_fund'
        else:
            table = 't_amac_manage'
        self.cursor.execute("truncate table "+table+"")
        self.conn.commit()

    count = 0
    def process_item(self, item, spider):
        self.count += 1

        if self.spidertype == 1:
            # t_amarc_manager_updates
            sql = 'insert into t_amac_fund_updates ' \
                  '(' \
                  'FUNDNAME, FUNDID, CHENGLI, BEIAN, BEIAN_JD, FUNDTYPE, BIZHONG, FUNDMANAGE,	MANAGETYPE,	' \
                  'TUOGUANMANAGE, STATUS, LASTUPDATETIME, REMARK, MONTH_R, HALFY_R, YEAR_R, QUARTER_R,	' \
                  'PARENTID,ID' \
                  ') ' \
                  'values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19)'
            values_list = [
                item['jjmc'], item['jjbh'], item['clsj'], item['basj'], item['bajd'], item['jjlx'],
                item['bz'], item['jjglrmc'], item['gllx'], item['tgrmc'], item['yzzt'], item['zhgxsj'],
                item['tbtx'], item['yb_dy'], item['yb_bnb'], item['yb_nb'], item['yb_jb'],
                item['glr_bh'], item['id']
            ]
        elif self.spidertype == 0:
            # t_amarc_fund_updates
            sql = 'insert into t_amac_manage(ID,MANAGERNAME,ARTIFICIALPERSONNAME,REGISTERNO,ESTABLISHDATE,' \
                  'MANAGERHASPRODUCT,URL,REGISTERDATE,REGISTERADDRESS,REGISTERPROVINCE,REGISTERCITY,REGADRAGG,' \
                  'FUNDCOUNT,FUNDSCALE,PAIDINCAPITAL,SUBSCRIBEDCAPITAL,HASSPECIALTIPS,INBLACKLIST,HASCREDITTIPS,' \
                  'REGCOORDINATE,OFFICECOORDINATE,OFFICEADDRESS,OFFICEPROVINCE,OFFICECITY,PRIMARYINVESTTYPE,' \
                  'EN_MANAGERNAME,ORG_CODE,ORG_TYPE,CREDITTIPS,REGISTERPAY,TUREPAY,PAYRATE,BUSINESSTYPE,STAFF,' \
                  'ISVIP,VIPTYPE,VIPTIME,LAWSTATUS,ISTOWORK,WORKWAY,LAWORG,LAWPER)' \
                  'values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,' \
                  ':25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35,:36,:37,:38,:39,:40,:41,:42)'
            values_list = [
                item['ID'], item['MANAGERNAME'], item['ARTIFICIALPERSONNAME'], item['REGISTERNO'],
                item['ESTABLISHDATE'], item['MANAGERHASPRODUCT'], item['URL'], item['REGISTERDATE'],
                item['REGISTERADDRESS'], item['REGISTERPROVINCE'], item['REGISTERCITY'], item['REGADRAGG'],
                item['FUNDCOUNT'], item['FUNDSCALE'], item['PAIDINCAPITAL'], item['SUBSCRIBEDCAPITAL'],
                item['HASSPECIALTIPS'], item['INBLACKLIST'], item['HASCREDITTIPS'], item['REGCOORDINATE'],
                item['OFFICECOORDINATE'], item['OFFICEADDRESS'], item['OFFICEPROVINCE'], item['OFFICECITY'],
                item['PRIMARYINVESTTYPE'], item['EN_MANAGERNAME'], item['ORG_CODE'], item['ORG_TYPE'],
                item['CREDITTIPS'], item['REGISTERPAY'], item['TUREPAY'], item['PAYRATE'], item['BUSINESSTYPE'],
                item['STAFF'], item['ISVIP'], item['VIPTYPE'], item['VIPTIME'], item['LAWSTATUS'], item['ISTOWORK'],
                item['WORKWAY'], item['LAWORG'], item['LAWPER']
            ]
        # print(sql)
        # print(", ".join('%s' % id for id in values_list))
        self.cursor.execute(sql, values_list)

        if self.count % 10000 == 0:
           self.conn.commit()

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def getconn(self):
        conn = cx_Oracle.connect('username/password@localhost/orcl')  # 连接数据库
        return conn