# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql import escape_string

class JianzhuPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password='a123456', db='jianzhu', charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.commit()


    def process_item(self, item, spider):
        # try:
            self.cursor.execute(
                "insert into scrapy(  url,company_name,project_name,project_code,project_address,date,province,city,intro,reference_number,reward_department,registration_department,telephone) values(%s ,%s, %s, %s ,%s ,%s, %s, %s, %s,%s,%s,%s,%s)",
                (
                    item["url"],
                    item['company_name'],
                    item['project_name'],
                    item['project_code'],
                    item['project_address'],
                    item['date'],
                    item['province'],
                    item['city'],
                    item['intro'],
                    item['reference_number'],
                    item['reward_department'],
                    item['registration_department'],
                    escape_string(item['telephone']),
                )
            )
            self.conn.commit()
        # except pymysql.Error:
        #     print("插入错误")

            return item


