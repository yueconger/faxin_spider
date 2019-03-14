# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
from lxml import etree
from scrapy.conf import settings
from conf import settings_init

class FaxinSpider(scrapy.Spider):
    name = 'faxin'
    allowed_domains = ['www.faxin.cn']
    start_urls = ['http://www.faxin.cn/']
    get_data_url = 'http://www.faxin.cn/lib/zyfl/GetZyflData.ashx'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'sid=otquuqu5xjb5uhfouyx01w3c; isAutoLogin=off; ASP.NET_SessionId=i2pjidhmtyu4aupiv0vk3w24; Hm_lvt_a317640b4aeca83b20c90d410335b70f=1552267033,1552353636,1552370693; Hm_lvt_a4967c0c3b39fcfba3a7e03f2e807c06=1552302923,1552353636,1552370694; Hm_lpvt_a4967c0c3b39fcfba3a7e03f2e807c06=1552370694; Hm_lpvt_a317640b4aeca83b20c90d410335b70f=1552370731',
        'Host': 'www.faxin.cn',
        'Origin': 'http://www.faxin.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.faxin.cn/lib/zyfl/ZyflLibrary.aspx?libid=010102',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    headers_detail = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.faxin.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    local_server = r'E:\LocalServer\Faxin_Law\国家_html\部门规章_new/'

    def start_requests(self):
        with open('conf.json', 'r', encoding='utf-8') as f:
            con = json.load(f)
        effect_path = con['effect_path'][3]
        for page in range(66, 71):
            page = str(page)
            form_data = "keyTitle=&keyContent=&fdep_id=&fwzh=&pdep_id=&sort_id=&xiaoli_id={effect_id}&Fdate_b=&Fdate_e=&Pdate_b=&Pdate_e=&shixiao_id=&Sdate_b=&Sdate_e=&searchtype=0&showsummary=undefined&ckbInSearch=undefined&lib=zyfl&chooseNum=&firstPage={page}&secondPage={page}&thirdPage={page}&fourthPage={page}&fifthPage={page}&sixthPage={page}&sort_field=-排序号,-发布日期&listnum=50&sort_id_left=&xiaoli_id_left=&shixiao_id_left=&fdep_id_left=&isAdvSearch=&usersearchtype=undefined"
            form_data = form_data.format(effect_id=effect_path['effect_id'], page=page)
            yield scrapy.Request(
                url=self.get_data_url,
                method='POST',
                body=form_data,
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        html = response.text
        try:
            res = json.loads(html)
        except:
            print('解析出错')
        else:
            html_con = res['SixthHtml']
            html_res = etree.HTML(html_con)
            try:
                li_list = html_res.xpath('//li/div[@class="fz-title1"]')
            except:
                print('内容不存在,抓取失败')
            else:
                print(li_list)
                for li in li_list:
                    law_url = li.xpath('./a/@href')[0]
                    print(law_url)
                    law_name = li.xpath('./a/text()')[0]
                    print(law_name, 'law_name')
                    law_url = 'http://www.faxin.cn/lib/zyfl/' + law_url
                    cookie = settings_init().random_cookie()
                    yield scrapy.Request(
                        url=law_url,
                        headers=self.headers_detail,
                        cookies=cookie,
                        meta={'law_url': law_url, 'law_name': law_name},
                        callback=self.parse_law,
                        dont_filter=True
                    )

    def parse_law(self, response):
        print('-----')
        law_name = response.meta['law_name']
        law_url = response.meta['law_url']
        name_id = response.meta['law_url'].split('gid=')[-1].split('&libid')[0]
        html = response.text
        verification_res = re.findall('您的访问频率过快，请稍后刷新！', html)
        if len(verification_res) > 0:
            print('访问过快')
            time.sleep(2)
            self.parse_law(response)
        else:
            if 'a class="login" href="/login.aspx"' in html:
                print('账号登录失败')
                self.parse_law_again(law_url, response)
            else:
                print('----------------------')
                file_name = self.local_server + law_name + '.html'

                try:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(html)
                except:
                    file_name = self.local_server + name_id + '.html'
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(html)
                print(law_name, '下载完毕!')

    def parse_law_again(self, law_url, response):
        cookie = settings_init().random_cookie()
        print(cookie)
        law_name = response.meta['law_name']
        yield scrapy.Request(
            url=law_url,
            headers=self.headers_detail,
            cookies=cookie,
            meta={'law_url': law_url, 'law_name': law_name},
            callback=self.parse_law,
            dont_filter=True
        )