# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import re
import time
import random
from lxml import etree
from CookiesPool.db import *

class FaxinSpider(scrapy.Spider):
    name = 'faxin_gat'
    allowed_domains = ['www.faxin.cn']
    start_urls = ['http://www.faxin.cn/']
    # city_url = 'http://www.faxin.cn/lib/xgk/GetHKflData.ashx'
    # city_url = 'http://www.faxin.cn/lib/twk/GetTWflData.ashx'
    city_url = 'http://www.faxin.cn/lib/amk/GetMACflData.ashx'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.faxin.cn',
        'Origin': 'http://www.faxin.cn',
        'Proxy-Connection': 'keep-alive',
        # 'Referer': 'http://www.faxin.cn/lib/xgk/HKflSearch.aspx?libid=',
        # 'Referer': 'http://www.faxin.cn/lib/twk/TWflContent.aspx?gid=',
        'Referer': 'http://www.faxin.cn/lib/amk/MACflSearch.aspx?libid=',
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
    local_server = r'E:\LocalServer\Faxin_Law\地方_html\澳门/'
    redis_client = RedisClient('cookies', 'faxin')

    db = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

    def start_requests(self):
        # with open('conf.json', 'r', encoding='utf-8') as f:
        #     con = json.load(f)
        # effect_path = con['effect_path'][3]
        for page in range(400, 471):
            page = str(page)
            # form_data = "keyTitle=&keyContent=&keyETitle=undefined&keyEContent=undefined&sort_id=&Fdate_b=undefined&Fdate_e=undefined&shixiao_id=undefined&searchtype=0&showsummary=undefined&ckbInSearch=undefined&lib=xgk&firstPage={page}&listnum=50&isAdvSearch=&usersearchtype=1"
            # form_data = "keyTitle=&keyContent=&keyETitle=undefined&keyEContent=undefined&sort_id=&Fdate_b=undefined&Fdate_e=undefined&shixiao_id=undefined&searchtype=0&showsummary=undefined&ckbInSearch=undefined&lib=twk&firstPage={page}&listnum=50&isAdvSearch=&usersearchtype=1"
            form_data = "keyTitle=&keyContent=&keyETitle=undefined&keyEContent=undefined&sort_id=&Fdate_b=undefined&Fdate_e=undefined&shixiao_id=undefined&searchtype=0&showsummary=undefined&ckbInSearch=undefined&lib=amk&firstPage={page}&listnum=50&isAdvSearch=&usersearchtype=1"
            # form_data = form_data.format(effect_id=effect_path['effect_id'], page=page)
            form_data = form_data.format(page=page)
            cookie = self.random_cookie()
            yield scrapy.Request(
                url=self.city_url,
                method='POST',
                body=form_data,
                cookies=cookie,
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
            html_con = res['FirstHtml']
            # print(html_con)
            html_res = etree.HTML(html_con)
            try:
                li_list = html_res.xpath('//li/div[@class="fz-title1"]')
            except:
                print('内容不存在,抓取失败')
            else:
                print(li_list)
                for li in li_list:
                    law_url = li.xpath('./a/@href')[0]
                    law_name = li.xpath('./a/text()')[0]
                    # law_url = 'http://www.faxin.cn/lib/xgk/' + law_url
                    # law_url = 'http://www.faxin.cn/lib/twk/' + law_url
                    law_url = 'http://www.faxin.cn/lib/amk/' + law_url
                    cookie = self.random_cookie()
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
                law_name = re.sub('/', '／', law_name)
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
        cookie = self.random_cookie()
        law_name = response.meta['law_name']
        yield scrapy.Request(
            url=law_url,
            headers=self.headers_detail,
            cookies=cookie,
            meta={'law_url': law_url, 'law_name': law_name},
            callback=self.parse_law,
            dont_filter=True
        )

    def random_cookie(self):
        redis_name = 'cookies:faxin'
        mm = random.choice(self.db.hvals(redis_name))
        cookie = json.loads(mm)
        return cookie