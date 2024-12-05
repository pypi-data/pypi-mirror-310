#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : md5.py
@Author: crawlSpider
@Address: https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%BD%91%E8%99%ABspider&ie=utf8&_sug_=n&_sug_type_=
@Github: https://github.com/qi20172017
@Date  : 2024/11/19 上午10:10
@Desc  : 根据提供的字符生成md5
"""

import hashlib
from minner.exceptions import UsageError
from minner.commands import MinnerCommand, BaseRunMinnerCommand

class Md5(BaseRunMinnerCommand):

    def run(self, args, opts):


        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError(
                "running 'scrapy crawl' with more than one spider is not supported"
            )
        spname = args[0] # 这是要启动爬虫的名字

        str_md5 = hashlib.md5(spname.encode(encoding='utf-8')).hexdigest()
        print(str_md5)
        return str_md5


if __name__ == '__main__':
    pass