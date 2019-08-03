# -*- coding: utf-8 -*-
import scrapy
import  urllib

class JianzhuSpider(scrapy.Spider):
    name = 'jianzhu'
    allowed_domains = ['59.175.169.110/web/']
    start_urls = ['http://59.175.169.110/web/corpCxxw/corpCxxwSearch.aspx?fl=1']


    def parse(self,response):
        # __EVENTARGUMENT = response.xpath("//input[@id='__EVENTARGUMENT']/@value").extract_first()
        __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        __EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
        # txtXm =  response.xpath("//input[@id='txtXm']/@value").extract_first()
        hfFl= response.xpath("//input[@name='hfFl']/@value").extract_first()
        hUrltype = response.xpath("//input[@name='hUrltype']/@value").extract_first()
        # txtPageIndex = response.xpath("//input[@name='txtPageIndex']/@value").extract_first()
        # next_page = response.xpath('//a[@id="lbtnNext"]/@href').extract_first()

        for page_num in range(1,28):
            form_data = dict(
                __EVENTTARGET=str('lbtngo'),
                # __EVENTARGUMENT = __EVENTARGUMENT,
                __VIEWSTATE = __VIEWSTATE,
                __EVENTVALIDATION = __EVENTVALIDATION,
                # txtXm = str(txtXm),
                ddlType= str(1),
                txtPageIndex=str(page_num),
                hUrltype =  str(hUrltype),
                hfFl=str(hfFl),

            )

            yield scrapy.FormRequest('http://59.175.169.110/web/corpCxxw/corpCxxwSearch.aspx?fl=1',
                                     formdata=form_data,
                                     callback=self.after_post,
                                     dont_filter=True
                                     )

    def after_post(self, response):
        # print(response.body.decode())
        url_list = response.xpath("//table[@id='tableList']//tr/td[2]/a/@href").extract()[0:-5]
        for url in url_list:
            url = urllib.parse.urljoin(response.url, url)
            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                dont_filter=True
            )
        print(url_list)

    def parse_detail(self, response):
        item = {}
        item["url"] = response.url
        item["company_name"] = response.xpath("//td[@id='corpName']/text()").extract_first()
        item["project_name"] = response.xpath("//td[@id='projName']/text()").extract_first()
        item["project_code"] = response.xpath("//td[@id='PrjNum']/text()").extract_first()
        item["project_address"] = response.xpath("//td[@id='Address']/text()").extract_first()
        item["date"] = response.xpath("//td[@id='AwardDate']/text()").extract_first()
        item["province"] = response.xpath("//td[@id='DSZ']/text()").extract_first()
        item["city"] = response.xpath("//td[@id='QX']/text()").extract_first()
        item["intro"] = response.xpath("//td[@id='txtJljj']/text()").extract_first()
        item["reference_number"] = response.xpath("//td[@id='AWARDNUMBER']/text()").extract_first()
        item["reward_department"] = response.xpath("//td[@id='AWARDDEPARTNAME']/text()").extract_first()
        item["registration_department"] = response.xpath("//td[@id='txtDjbm']/text()").extract_first()
        item["telephone"] = response.xpath("//td[@id='txtDjbmLxdh']/text()").extract_first()
        yield item
        # print(item)
