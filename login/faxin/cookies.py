# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 10:24
# @Author  : yueconger
# @File    : cookies.py

import time
import requests


class FaxinCookies(object):
    def __init__(self, username, password):
        self.login_url = "http://www.faxin.cn/login.aspx"
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
        self.username = username
        self.password = password

    def set_formdata(self, username, password):
        form_data = {
            '__VIEWSTATE': '/wEPDwUJMTg3MTkxMzg4ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUKaXNSZW1lbWJlcgULaXNBdXRvTG9naW4=',
            'WebUCHead_Special1$hiddIsLogin': '0',
            'WebUCSearchNoAdvSearch1$lib': '',
            'keyword': '',
            'user_name': username,
            'user_password': password
        }
        return form_data

    def get_cookies(self, form_data):
        response = requests.post(url=self.login_url, headers=self.headers, data=form_data, allow_redirects=False)
        html = response.content.decode()
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        if 'lawapp_web' in str(cookies):
            """登录正常, 入库"""
            return {
                'status': 1,
                'content': cookies
            }
        else:
            if '登录用户已超出在线数' in html:
                return {
                    'status': 3,
                    'content': '此账号已登录'
                }
            else:
                return {
                    'status': 2,
                    'content': '用户名或密码错误'
                }

    def main(self):
        form_data = self.set_formdata(self.username, self.password)
        cookie_info = self.get_cookies(form_data)
        return cookie_info


if __name__ == '__main__':
    result = FaxinCookies('chen_03', 'chen_03').main()
    print(result)
