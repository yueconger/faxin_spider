# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 10:23
# @Author  : yueconger
# @File    : importer.py
import requests

from CookiesPool.db import RedisClient

conn = RedisClient('accounts', 'faxin')


def set(account, sep='----'):
    """账号信息格式提前设置为 username----password"""
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入账号密码组, 输入exit退出读入')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    scan()
