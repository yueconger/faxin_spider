# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 9:11
# @Author  : yueconger
# @File    : conf.py
import requests
import json
import re
import time


class settings_init(object):
    def __init__(self):
        self.homepage_url = 'http://www.faxin.cn/search/GeneralLawSearch.aspx'
        self.login_url = 'http://www.faxin.cn/login.aspx'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.faxin.cn',
            'Referer': 'http://www.faxin.cn/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        self.formdata = "WebUCHead_Special1%24hiddIsLogin=0&WebUCSearchNoAdvSearch1%24lib=&keyword=&user_name=394044548%40qq.com&user_password=zjt19921116"
    def get_session(self):
        url = self.homepage_url
        s = requests.Session()
        response = s.get(url, headers=self.headers)
        session = response.cookies
        cookies = session.items()
        cookie = '='.join(list(cookies[0]))
        return cookie

    def login_in(self):
        cookie = "ASP.NET_SessionId=otquuqu5xjb5uhfouyx01w3c; Hm_lvt_a317640b4aeca83b20c90d410335b70f=1552267033,1552353636; Hm_lvt_a4967c0c3b39fcfba3a7e03f2e807c06=1552302923,1552353636; sid=otquuqu5xjb5uhfouyx01w3c; isAutoLogin=off; lawapp_web=9F4659AFF9827CA8364C171FDF69856D5E8EB49BA8F88BF7FDC058FCD8A75A9349291AFE75CB2DCB424CD93BD9FF4C9E42D341E05448ECA5E83F9CD1CF22292EF3E9B001B09E37487349FCC91A693636F6A47FB297A7280DA15B405EA8C4ACFE3818BF7398972C57B445F4F1E81EA040304555FA3E8AFF3C5EEC3C49049ED563A6754E9953AE61A8D4CCCE563C518402697368426F8EA00614C8052DB702C7666E54AB98; Hm_lpvt_a4967c0c3b39fcfba3a7e03f2e807c06=1552358530; Hm_lpvt_a317640b4aeca83b20c90d410335b70f=1552358732"
        headers = self.headers
        headers['Cookie'] = cookie
        response = requests.post(self.login_url, data=self.formdata, headers=headers)
        # return response.content.decode()
        # cookies = response.cookies
        # return cookies

        index_url = 'http://www.faxin.cn/index.aspx'
        res = requests.get(index_url, headers=headers)
        coo = res.cookies
        print(coo.items())
        return res.content.decode()



if __name__ == '__main__':
    settings_init = settings_init()
    # cookie = settings_init.get_session()
    # print(cookie)
    res = settings_init.login_in()
    print(res)