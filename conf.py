# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 9:11
# @Author  : yueconger
# @File    : conf.py
import requests
import json
import random
import re
import time
from selenium import webdriver
import time


class settings_init(object):
    def __init__(self):
        self.homepage_url = 'http://www.faxin.cn/index.aspx'
        self.login_url = 'http://www.faxin.cn/login.aspx'
        self.login_out_url = 'http://www.faxin.cn/login.aspx'
        self.check_url = 'http://www.faxin.cn/user/check_user.ashx'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.faxin.cn',
            'Referer': 'http://www.faxin.cn/login.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }

    def set_formdata(self, user_name, user_password):
        form_data = {
            '__VIEWSTATE': '/wEPDwUJMTg3MTkxMzg4ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUKaXNSZW1lbWJlcgULaXNBdXRvTG9naW4=',
            'WebUCHead_Special1$hiddIsLogin': '0',
            'WebUCSearchNoAdvSearch1$lib': '',
            'keyword': '',
            'user_name': user_name,
            'user_password': user_password
        }
        return form_data

    def check_status(self, form_data):
        response = requests.post(url=self.check_url, headers=self.headers, data=form_data, allow_redirects=False)
        print(response.content.decode())

    def get_cookies(self, form_data):
        res = requests.post(url=self.login_url, headers=self.headers, data=form_data, allow_redirects=False)
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        print(cookies)
        html = res.content.decode()
        print(res.content.decode())
        if 'lawapp_web' in str(cookies):
            print('登录正常, 入库')

            with open('cookies.txt', 'a+', encoding='utf-8') as f:
                f.write(str(cookies) + '\n')
        else:
            print('登录失败')
            if '登录用户已超出在线数' in html:
                print('此账号已登录')
            else:
                print('账号出错')
            self.check_status(form_data)

    def login_selenium(self):
        browser = webdriver.Chrome()
        browser.get(self.login_url)
        browser.find_elements_by_xpath('//input[@name="user_name"]')[0].send_keys('miao2019')
        browser.find_elements_by_xpath('//input[@name="user_password"]')[0].send_keys('13245768')
        browser.find_elements_by_xpath('//input[@name="button"]')[0].click()
        time.sleep(1)
        cookies = requests.utils.dict_from_cookiejar(browser.get_cookies())
        print(cookies)

    def random_cookie(self):
        url = "http://127.0.0.1:5000/faxin/random"
        response = requests.get(url)
        html = response.content.decode()
        cookie = json.loads(html)
        return cookie


if __name__ == '__main__':
    settings_init = settings_init()
    # settings_init.random_cookie()

    # with open('./FaxinSpider/password.json') as jf:
    #     account_list = json.load(jf)
    # # random_num = random.randint(0, len(account_list))
    # for random_num in range(len(account_list)):
    #     user_name, user_password = account_list[random_num].values()
    #     print(user_name, user_password)
    #     form_data = settings_init.set_formdata(user_name, user_password)
    #     settings_init.get_cookies(form_data)