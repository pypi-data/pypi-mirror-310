#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : cmdline.py
@Author: crawlSpider
@Address: https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%BD%91%E8%99%ABspider&ie=utf8&_sug_=n&_sug_type_=
@Github: https://github.com/qi20172017
@Date  : 2024/11/19 下午3:00
@Desc  : 
"""

import argparse
import cProfile
import inspect  # 模块提供了一些有用的函数帮助获取对象的信息，可以判断某个对象是什么类型，还可以返回某个对象的代码
import os
import sys

import pkg_resources

import minner
# from scrapy.commands import BaseRunSpiderCommand, ScrapyCommand, ScrapyHelpFormatter
# from scrapy.crawler import CrawlerProcess
from minner.exceptions import UsageError
# from scrapy.utils.misc import walk_modules
# from scrapy.utils.project import get_project_settings, inside_project
# from scrapy.utils.python import garbage_collect

from importlib import import_module
from pkgutil import iter_modules
from minner.commands import MinnerCommand

class ScrapyArgumentParser(argparse.ArgumentParser):
    def _parse_optional(self, arg_string):
        # if starts with -: it means that is a parameter not a argument
        if arg_string[:2] == "-:":
            return None

        return super()._parse_optional(arg_string)

def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('scrapy.utils')
    """

    mods = []
    mod = import_module(path)   # 就是导入这个包
    mods.append(mod)
    if hasattr(mod, "__path__"):  # 根据定义，如果一个模块具有 __path__ 属性，它就是包。
        for _, subpath, ispkg in iter_modules(mod.__path__): # 为 path 上的所有子模块产生 ModuleInfo，pkgutil 该模块为导入系统提供了工具，尤其是在包支持方面。

            fullpath = path + "." + subpath
            if ispkg:
                mods += walk_modules(fullpath)  # 列表的拓展可以直接这样 + ,效果和extend是一样的
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods

def _iter_command_classes(module_name):
    # TODO: add `name` attribute to commands and merge this function with
    for module in walk_modules(module_name):
        for obj in vars(module).values(): # 返回模块、类、实例或任何其它具有 __dict__ 属性的对象的 __dict__ 属性。
            if (
                inspect.isclass(obj)  # 判断obj是不是一个类
                and issubclass(obj, MinnerCommand)   # obj是否是ScrapyCommand的子类
                and obj.__module__ == module.__name__
                and obj not in (MinnerCommand,)
            ):
                yield obj



def _get_commands_from_module(module, inproject):
    d = {}
    for cmd in _iter_command_classes(module):
        # if inproject or not cmd.requires_project:
        if True:
            cmdname = cmd.__module__.split(".")[-1]
            d[cmdname] = cmd()  # 在这里把命令类，实例化
    return d


def _get_commands_from_entry_points(inproject, group="scrapy.commands"):
    cmds = {}
    for entry_point in pkg_resources.iter_entry_points(group):
        obj = entry_point.load()
        if inspect.isclass(obj):
            cmds[entry_point.name] = obj()
        else:
            raise Exception(f"Invalid entry point {entry_point.name}")
    return cmds


def _get_commands_dict(settings, inproject):
    cmds = _get_commands_from_module("minner.commands", inproject)
    # cmds.update(_get_commands_from_entry_points(inproject))
    # cmds_module = settings["COMMANDS_MODULE"]
    # if cmds_module:
    #     cmds.update(_get_commands_from_module(cmds_module, inproject))
    return cmds


def _pop_command_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith("-"):
            del argv[i]
            return arg
        i += 1


def _print_header(settings, inproject):
    version = minner.__version__
    if inproject:
        print(f"Scrapy {version} - active project: {settings['BOT_NAME']}\n")

    else:
        print(f"Scrapy {version} - no active project\n")


def _print_commands(settings, inproject):
    _print_header(settings, inproject)
    print("Usage:")
    print("  scrapy <command> [options] [args]\n")
    print("Available commands:")
    cmds = _get_commands_dict(settings, inproject)
    for cmdname, cmdclass in sorted(cmds.items()):
        print(f"  {cmdname:<13} {cmdclass.short_desc()}")
    if not inproject:
        print()
        print("  [ more ]      More commands available when run from project directory")
    print()
    print('Use "scrapy <command> -h" to see more info about a command')


def _print_unknown_command(settings, cmdname, inproject):
    _print_header(settings, inproject)
    print(f"Unknown command: {cmdname}\n")
    print('Use "scrapy" to see available commands')


def _run_print_help(parser, func, *a, **kw):
    try:
        func(*a, **kw)
    except UsageError as e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)


def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv

    settings = 1
    if settings is None:

        try:
            editor = os.environ["EDITOR"]
        except KeyError:
            pass
        else:
            settings["EDITOR"] = editor

    # inproject = inside_project()
    cmds = _get_commands_dict(settings, '')  # 把命令系统命令和自定义命令取出来放到字典里
    cmdname = _pop_command_name(argv)  # 取出用户调用的命令
    if not cmdname:
        _print_commands(settings, '')
        sys.exit(0)
    elif cmdname not in cmds:
        _print_unknown_command(settings, cmdname, '')
        sys.exit(2)

    cmd = cmds[cmdname]  # 根据具命令名字取出命令执行的对象
    parser = ScrapyArgumentParser(
        # formatter_class=ScrapyHelpFormatter,
        usage=f"scrapy {cmdname} {cmd.syntax()}",
        conflict_handler="resolve",
        description=cmd.long_desc(),
    )

    # settings.setdict(cmd.default_settings, priority="command")  # 在创建命令对象的时候，有个设置的类属性，这里是把这些设置给添加到系统设置上
    # cmd.settings = settings
    cmd.add_options(parser)  # 其实为parser对象添加命令参数
    opts, args = parser.parse_known_args(args=argv[1:]) # 再次取出用户调用的命令参数
    # _run_print_help(parser, cmd.process_options, args, opts)  # 把命令行中设置的参数添加到系统设置中

    # cmd.crawler_process = CrawlerProcess(settings)  # 给命令对象添加CrawlerProcess
    _run_print_help(parser, _run_command, cmd, args, opts) # 通过cmd的run调用crawler_process的start，从而启动
    sys.exit(cmd.exitcode)


def _run_command(cmd, args, opts):
    if opts.profile:
        _run_command_profiled(cmd, args, opts)
    else:
        cmd.run(args, opts)


def _run_command_profiled(cmd, args, opts):
    if opts.profile:
        sys.stderr.write(f"scrapy: writing cProfile stats to {opts.profile!r}\n")
    loc = locals()
    p = cProfile.Profile()
    p.runctx("cmd.run(args, opts)", globals(), loc)
    if opts.profile:
        p.dump_stats(opts.profile)


if __name__ == "__main__":
    try:
        execute()
    finally:
        # Twisted prints errors in DebugInfo.__del__, but PyPy does not run gc.collect() on exit:
        # http://doc.pypy.org/en/latest/cpython_differences.html
        # ?highlight=gc.collect#differences-related-to-garbage-collection-strategies
        # garbage_collect()

        pass

