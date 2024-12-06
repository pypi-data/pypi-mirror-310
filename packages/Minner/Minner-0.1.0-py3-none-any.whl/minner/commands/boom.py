#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : boom.py
@Author: crawlSpider
@Address: https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%BD%91%E8%99%ABspider&ie=utf8&_sug_=n&_sug_type_=
@Github: https://github.com/qi20172017
@Date  : 2024/11/22 上午11:35
@Desc  : 
"""


import hashlib
from minner.exceptions import UsageError
from minner.commands import BaseRunMinnerCommand

class Boom(BaseRunMinnerCommand):

    def boom(self, all_money, y_money, m_money, all_y, rate):

        if all_money:
            y_money = int(all_money / all_y)
        elif m_money:
            y_money = m_money * 12

        final = y_money

        for i in range(1, int(all_y + 1)):
            final = final * (1 + rate)

            raw_money = i * y_money
            print(f'第{i}年： {raw_money}, {final}')
            final = final + y_money

    def add_options(self, parser):
        super().add_options(parser)

        parser.add_argument(
            # '-r',
            'rate',
            type=float,
            help='年收益率'
        )

        parser.add_argument(
            # '-y',
            'years',
            type=float,
            help='投资年限'
        )

        parser.add_argument(
            '-a',
            '--all_money',
            type=float
        )
        parser.add_argument(
            '-n',
            '--n_money',
            type=float
        )
        parser.add_argument(
            '-m',
            '--m_money',
            type=float
        )



    def run(self, args, opts):


        # if len(args) < 1:
        #     raise UsageError()
        # elif len(args) > 1:
        #     raise UsageError(
        #         "running 'scrapy crawl' with more than one spider is not supported"
        #     )
        # spname = args[0] # 这是要启动爬虫的名字


        self.boom(opts.all_money, opts.n_money, opts.m_money, opts.years, opts.rate)

        # str_md5 = hashlib.md5(spname.encode(encoding='utf-8')).hexdigest()
        # print(spname)
        # return str_md5


