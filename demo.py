# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 16:43
# @Author  : yueconger
# @File    : demo.py
import redis
import json
import random
db = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
redis_name = 'cookies:faxin'
mm = random.choice(db.hvals(redis_name))
print(mm)
a = json.loads(mm)
print(a)