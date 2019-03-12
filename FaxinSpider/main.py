# -*- coding: utf-8 -*-
# @Time    : 2018/9/3 14:27
# @Author  : XiZhi
# @File    : main.py
import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "faxin"])
