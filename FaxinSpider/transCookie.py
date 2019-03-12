# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 15:52
# @Author  : yueconger
# @File    : transCookie.py
# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


if __name__ == "__main__":
    cookie = 'isAutoLogin=off; ASP.NET_SessionId=i2pjidhmtyu4aupiv0vk3w24; Hm_lvt_a317640b4aeca83b20c90d410335b70f=1552267033,1552353636,1552370693; Hm_lvt_a4967c0c3b39fcfba3a7e03f2e807c06=1552302923,1552353636,1552370694; sid=i2pjidhmtyu4aupiv0vk3w24; lawapp_web=1C39241FF3B0864EC82E5009D4896E20253540AE1EFF5660F223CFADE54E9C41A2CF76EADB39F318257865C28FB028B3390449554A6A18B2A0E6CB99EC608523B7460EF4C42472107E89F21A8945A1BCDADA6E2AB9D5BA34518C208A4AA52016C892028E8DF328396A4EF3F1196D8C401E8AC80408D82F2699D08D10EB98F87B327668951FD28C8A45C03DCB004DD894DF1E45C0424B4113A121B2A6317AD17F99A90920; Hm_lpvt_a4967c0c3b39fcfba3a7e03f2e807c06=1552376125; Hm_lpvt_a317640b4aeca83b20c90d410335b70f=1552376534'
    trans = transCookie(cookie)
    print(trans.stringToDict())
