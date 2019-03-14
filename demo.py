# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 16:43
# @Author  : yueconger
# @File    : demo.py
import requests

url = 'http://www.faxin.cn/login.aspx'
form_data = {
    '__VIEWSTATE': '/wEPDwUJMTg3MTkxMzg4ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUKaXNSZW1lbWJlcgULaXNBdXRvTG9naW4=',
    'WebUCHead_Special1$hiddIsLogin': '0',
    'WebUCSearchNoAdvSearch1$lib': '',
    'keyword': '',
    'user_name': 'hahazhang',
    'user_password': 'zhanghaha123'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

res = requests.post(url, headers=headers, data=form_data, allow_redirects=False)
cookies = requests.utils.dict_from_cookiejar(res.cookies)
print(cookies)
print(res.content.decode())
if 'lawapp_web' in str(cookies):
    print('登录正常, 入库')

    with open('cookies.txt', 'a+', encoding='utf-8') as f:
        f.write(str(cookies) + '\n')
else:
    print('')

# s = requests.Session()
# response = s.get(url, headers=headers)
# session = response.cookies
# cookies = session.items()
# cookie = '='.join(list(cookies[0]))
# res = requests.post(url, headers=headers, data=form_data, allow_redirects=False)
# cookies = requests.utils.dict_from_cookiejar(res.cookies)
# print(cookies)
# print(res.content.decode())


cookies = {'lawapp_web': '28DB4C4AF768DBFE12D90B0A6C1B9A714BA1ADE59681F6D609918BDFCA477298B7D09DDA4CC4DE9D25A5C0B5E8D2175C89B667B4B78C5FB4EA236560C64E756A290B31D3EC9DAF071D66A574541CF27F54E3E455B6107E5AC2BDF4133C4DEF5EE54EBED78FCD56C890F1549F91FD2F4AF617DD70435FFDE312F4C7D2B10FC34AFDA06E4F995B8E8EDC7B919FD3641F47C50AA70B', 'ASP.NET_SessionId': '5xizgyximvvpmidms5tlgchd', 'sid': '5xizgyximvvpmidms5tlgchd'}

detail_url = 'http://www.faxin.cn/lib/lfsf/LfContent.aspx?gid=G21694&libid=all'
response = requests.get(detail_url, headers=headers, cookies=cookies)
print(response.content.decode())
print(response.cookies)
