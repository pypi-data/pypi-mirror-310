#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : 1.py
@Author: crawlSpider
@Address: https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%BD%91%E8%99%ABspider&ie=utf8&_sug_=n&_sug_type_=
@Github: https://github.com/qi20172017
@Date  : 2024/11/18 下午5:53
@Desc  : 
"""

import psutil

# res = psutil.cpu_times()
res = psutil.cpu_count()

print(res)

# if __name__ == '__main__':
#     pass