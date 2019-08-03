# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import re
import json
from copy import deepcopy


class ZizhiSpider(scrapy.Spider):
    name = 'zizhi'
    # allowed_domains = ['nxjscx.com.cn/qysj.htm#']
    start_urls = ['http://218.95.173.11:8092/jzptweb/company_list.html?qualification=1&islocal=JN01']

    def parse(self, response):
        for page_num in range(1,6):
            form_data = dict(

                page=page_num,
                resid='web_company.quaryCorp',
                ci_qualification_code=str(1),
                ci_islocal_code='JN01',
                rows=str(15)
            )
            url = "http://218.95.173.11:8092/portal.php?" + urlencode(form_data)
            yield scrapy.Request(
                url=url,
                callback=self.after_post,
                # dont_filter=True
            )

    def after_post(self, response):
        # print('*'*100)
        # print(response.url)
        # print(response.body.decode())
        # id_list = re.findall('"id":"(.*?)"',response.body.decode())
        corp_id_list = re.findall('"corp_id":"(.*?)"', response.body.decode())

        # print(id_list)
        print(corp_id_list)
        item = {}
        # item["name"] = []
        # # # item["originalurl"] = []
        # item["zizhiname"] = []
        # item["zizhileibie"] = []
        # item["zhengshuhao"] = []
        # item["fazhengriqi"] = []
        # item["youxiaoqi"] = []
        # item["fazhengjigou"] = []
        # item["img_list"] = []
        # item["video_list"] = []http://218.95.173.11:8092/selectact/query.jspx?page=1&resid=IDJBYUVHL9&corp_id=2012100999&rows=10

        for corp_id in corp_id_list:  # 公司信息http://218.95.173.11:8092/selectact/query.jspx?resid=IDIXWP2KBO&rowid=2012100837-10NU1S2U&rows=10
            form_data = dict(
                page=str(1),
                resid='IDJBYUVHL9',
                corp_id=corp_id,
                rows='10'
            )
            url = 'http://218.95.173.11:8092/selectact/query.jspx?' + urlencode(form_data)
            yield scrapy.Request(
                url=url,
                callback=self.get_detail1,
                # dont_filter= True,
                meta={"corp_id": corp_id}
            )
        # for corp_id in corp_id_list:#资质信息
        #     form_data1 = dict(
        #         resid='IDIXWTKRCN',
        #         corp_id=corp_id,
        #         rows='10'
        #     )
        #     url = 'http://218.95.173.11:8092/selectact/query.jspx?' + urlencode(form_data1)
        #     yield scrapy.Request(
        #         url=url,
        #         callback=self.get_detail2,
        #         # dont_filter=True,
        #         meta={"item": item}
        #     )
        # for corp_id in corp_id_list:#证书信息
        #     form_data2 = dict(
        #         page = str(1),
        #         resid='IDJ2IDTKGL',
        #         fk_corp_id= corp_id ,
        #         rows='10'
        #     )
        #     url1 = 'http://218.95.173.11:8092/selectact/query.jspx?' + urlencode((form_data2))
        #     yield scrapy.Request(
        #         url=url1,
        #         callback=self.get_detail3,
        #         # dont_filter=True,
        #         meta={"item": item}
        #     )
        # print(item)
        # yield item

    def get_detail1(self, response):
        item1 = {}
        corp_id = response.meta["corp_id"]
        # for corp_id in corp_id_list:
        rt = json.loads(response.body.decode())
        name = rt["data"][0]["ci_name"]
        form_data23 = dict(
            id=rt["data"][0]["id"],
            corp_id=rt["data"][0]["corp_id"],
        )
        originalurl = 'http://218.95.173.11:8092/jzptweb/company_detail.html?' + urlencode(form_data23)
        print(originalurl)
        item1["originalurl"] = originalurl
        item1["name"] = name

        form_data1 = dict(
            page=str(1),
            resid='IDJ2IDTKGL',
            fk_corp_id=corp_id,
            rows='10'
        )
        url = 'http://218.95.173.11:8092/selectact/query.jspx?' + urlencode(form_data1)

        yield scrapy.Request(
            url=url,
            callback=self.get_detail2,
            # dont_filter=True,
            meta={"item1": item1, "corp_id": corp_id}
        )

    def get_detail2(self, response):
        item1 = response.meta["item1"]
        corp_id = response.meta["corp_id"]
        rt = json.loads(response.body.decode())
        if len(rt["data"]) > 0:
            for i in range(0, len(rt["data"])):
                zhengshuhao = rt["data"][i][("cl_code")]
                fazhengriqi = rt["data"][i]["cl_issue_date"]
                youxiaoqi1 = rt["data"][i]["cl_valid_sdate"]
                youxiaoqi2 = rt["data"][i]["cl_valid_edate"]
                fazhengjigou = rt["data"][i]["cl_issue_orga"]
                item1["zhengshuhao"] = zhengshuhao
                item1["fazhengriqi"] = fazhengriqi
                item1["youxiaoqi"] = (youxiaoqi1 + '-' + youxiaoqi2)
                item1["fazhengjigou"] = fazhengjigou
        else:
            item1["zhengshuhao"] = '0'
            item1["fazhengriqi"] = '0'
            item1["youxiaoqi"] = '0'
            item1["fazhengjigou"] = '0'
            # print(type(item["youxiaoqi"]))
            # print(type(fazhengjigou))
        form_data2 = dict(

            resid='IDIXWTKRCN',
            corp_id=corp_id,
            rows='10'
        )
        url = 'http://218.95.173.11:8092/selectact/query.jspx?' + urlencode(form_data2)
        yield scrapy.Request(
            url=url,
            callback=self.get_detail3,
            # dont_filter=True,
            meta={"item1": item1, "corp_id": corp_id}
        )

    def get_detail3(self, response):
        item = response.meta["item1"]
        corp_id = response.meta["corp_id"]
        rt = json.loads(response.body.decode())

        # for k in range(0,15):
        for i in range(0, len(rt["data"])):
            # if len(rt["data"]) is not None:
            #     if len(rt["data"][i]["cq_type"]) is not None:
                a = rt["data"][i]["cq_type"]
            #     else:
            #         a = ''
                # print(zizhiname)
                # print(type(zizhiname))
                # item["zizhiname"]=([(zizhiname)])
                if rt["data"][i]["cqs_sequence"] is not None:
                    b = rt["data"][i]["cqs_sequence"]
                else:
                    b = ''
                if rt["data"][i]["cqs_speciality"] is not None:
                    c = rt["data"][i]["cqs_speciality"]
                else:
                    c = ''
                if rt["data"][i]["cqs_level"] is not None:
                    d = rt["data"][i]["cqs_level"]
                else:
                    d = ''

                zizhileibie1 = b + c + d
                # zizhileibie2 = rt["data"][i]["cqs_speciality"]
                # zizhileibie3 = rt["data"][i]["cqs_level"]
                #     a=a.insert(-1,c)
                #     b=b.insert(-1,(zizhileibie1, zizhileibie2, zizhileibie3))
                # for x,y in a,b:

                item["name"] = item["name"]
                item["zizhiname"] = a
                item["zizhileibie"] = zizhileibie1
                item["originalurl"] = item["originalurl"]
                item["zhengshuhao"] = item["zhengshuhao"]
                item["fazhengriqi"] = item["fazhengriqi"]
                item["youxiaoqi"] = item["youxiaoqi"]
                item["fazhengjigou"] = item["fazhengjigou"]
            # else:
            #     item["name"] = item["name"]
            #     item["zizhiname"] = '0'
            #     item["zizhileibie"] = '0'
            #     item["originalurl"] = item["originalurl"]
            #     item["zhengshuhao"] = item["zhengshuhao"]
            #     item["fazhengriqi"] = item["fazhengriqi"]
            #     item["youxiaoqi"] = item["youxiaoqi"]
            #     item["fazhengjigou"] = item["fazhengjigou"]

                yield item
    #     item["zhengshuhao"].extend(re.findall('"cl_code":"(.*?)"',response.body.decode()))
    #     item["fazhengriqi"].extend(re.findall('"cl_issue_date":"(.*?)"',response.body.decode()))
    #     # time1 = re.findall('"cl_valid_sdate":"(.*?)"', response.body.decode())[0] if len(
    #     #     re.findall('"cl_valid_sdate":"(.*?)"', response.body.decode())[0]) > 0 else None
    #     # time2 = re.findall('"cl_valid_edate":"(.*?)"', response.body.decode())[0] if len(
    #     #     re.findall('"cl_valid_edate":"(.*?)"', response.body.decode())[0]) > 0 else None
    #     item["youxiaoqi"].extend(re.findall('"cl_valid_edate":"(.*?)"',response.body.decode()))
    #     item["fazhengjigou"].extend(re.findall('"cl_issue_orga":"(.*?)"',response.body.decode()))
    #     print(item)
    #     yield item
