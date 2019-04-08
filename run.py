# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 11:34
# @Author  : yueconger
# @File    : run.py

from CookiesPool.scheduler import Scheduler


def main():
    """cookie池维护启动"""
    s = Scheduler()
    s.run()


if __name__ == '__main__':
    main()
