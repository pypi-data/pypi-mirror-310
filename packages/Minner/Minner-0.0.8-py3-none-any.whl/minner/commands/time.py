#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : time.py
@Author: crawlSpider
@Address: https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%BD%91%E8%99%ABspider&ie=utf8&_sug_=n&_sug_type_=
@Github: https://github.com/qi20172017
@Date  : 2024/11/19 下午2:13
@Desc  : 打印当前时间
"""
import time
import datetime
import hashlib
from minner.exceptions import UsageError
from minner.commands import MinnerCommand, BaseRunMinnerCommand

class Time(BaseRunMinnerCommand):

    def run(self, args, opts):


        # if len(args) < 1:
        #     raise UsageError()
        # elif len(args) > 1:
        #     raise UsageError(
        #         "running 'scrapy crawl' with more than one spider is not supported"
        #     )
        # spname = args[0] # 这是要启动爬虫的名字


        today = datetime.datetime.now().strftime('%Y-%m-%d')

        print(today)
        return today

if __name__ == '__main__':
    pass