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
                '''insert into copy(name,originalurl,zizhiname,zizhileibie,zhengshuhao,fazhengriqi,youxiaoqi,fazhengjigou)  values(%s,%s,%s,%s,%s,%s,%s,%s)''',
                (
                    str(item['name']),
                    str(item["originalurl"]),
                    str(item['zizhiname']),
                    str(item['zizhileibie']),
                    str(item['zhengshuhao']),
                    str(item['fazhengriqi']),
                    str(item['youxiaoqi']),
                    str(item['fazhengjigou']),
                )
            )
            self.conn.commit()
        # except pymysql.Error:
        #     print("插入错误")

            return item
