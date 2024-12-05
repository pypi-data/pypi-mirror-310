#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : __init__.py.py
@Author: crawlSpider
@Address: https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%BD%91%E8%99%ABspider&ie=utf8&_sug_=n&_sug_type_=
@Github: https://github.com/qi20172017
@Date  : 2024/11/18 下午5:27
@Desc  : 
"""
import os
from twisted.python import failure

from pathlib import Path

from typing import Any, Dict, Optional
from minner.exceptions import UsageError


def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split("=", 1) for x in arglist)


class MinnerCommand:
    requires_project = False
    # crawler_process: Optional[CrawlerProcess] = None   # Optional的作用就是提示一下，这个变量的数据类型可以是这个类，最好是这个类型，如果非要传入其他类型，传还是可以传的，所以只是提示一下，最好传这个类型

    # default settings to be used for this command instead of global defaults
    default_settings: Dict[str, Any] = {}

    exitcode = 0

    def __init__(self) -> None:
        self.settings: Any = None  # set in scrapy.cmdline

    def set_crawler(self, crawler):
        if hasattr(self, "_crawler"):
            raise RuntimeError("crawler already set")
        self._crawler = crawler

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines since no post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """                                                        # add_argument_group就是创建一个容放命令的分组。这个分组在help的文本描述中会单独成段落
        group = parser.add_argument_group(title="Global Options", description="Build in parent class: ScrapyCommand")
        group.add_argument(                                        # group对象和一般的parser对象一样，添加参数，只不过group添加的参数，加入了自己的分组。parser就是常规加了个参数
            "--logfile", metavar="FILE", help="log file. if omitted stderr will be used" # add_argument_group有title参数，还有description参数，用于添加描述
        )                                           # metavar 是显示帮助的时候，显示的占位变量的名字
        group.add_argument(
            "-L",
            "--loglevel",
            metavar="LEVEL",  # metaver用来显示名字的，在帮助里面
            default=None,   # 默认值
            # help=f"log level (default: {self.settings['LOG_LEVEL']})",
        )
        group.add_argument(  #action 有很多值，表示不同的行为，这个store_true表示使用这个--nolog参数的时候，这个变量nolog的值为true
            "--nolog", action="store_true", help="disable logging completely"
        )
        group.add_argument(
            "--profile",
            metavar="FILE",
            default=None,
            help="write python cProfile stats to FILE",
        )
        group.add_argument("--pidfile", metavar="FILE", help="write process ID to FILE")
        group.add_argument(
            "-s",
            "--set",
            action="append",   # 表示可多次使用-s参数，每次使用就往一个列表中添加一下这个设置值
            default=[],
            metavar="NAME=VALUE",
            help="set/override setting (may be repeated)",
        )
        group.add_argument("--pdb", action="store_true", help="enable pdb on failure")

    def process_options(self, args, opts):
        try:
            self.settings.setdict(arglist_to_dict(opts.set), priority="cmdline")
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)

        if opts.logfile:
            self.settings.set("LOG_ENABLED", True, priority="cmdline")
            self.settings.set("LOG_FILE", opts.logfile, priority="cmdline")

        if opts.loglevel:
            self.settings.set("LOG_ENABLED", True, priority="cmdline")
            self.settings.set("LOG_LEVEL", opts.loglevel, priority="cmdline")

        if opts.nolog:
            self.settings.set("LOG_ENABLED", False, priority="cmdline")

        if opts.pidfile:
            Path(opts.pidfile).write_text(
                str(os.getpid()) + os.linesep, encoding="utf-8"
            )

        if opts.pdb:
            failure.startDebugMode()

    def run(self, args, opts):
        """
        Entry point for running commands
        """
        raise NotImplementedError  # 表示子类要重新实现这个方法


class BaseRunMinnerCommand(MinnerCommand):

    def add_options(self, parser):
        MinnerCommand.add_options(self, parser)
        parser.add_argument(
            "-s",
            "--square",
            # type=int,
            help="display a square of a given number"
        )


if __name__ == '__main__':
    pass