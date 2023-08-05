# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/10/29 10:35
# @Author  : derek
# @File    : all.py
# @Version : 1.0
# 说明:
import importlib
import logging

from cjtmc_base.utils.error import FileClassNotFoundError

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class AllBase():
    """
    使用继承来实现，通过重构父进程的方法来实现传参
    """

    def __init__(self, origin, region='cn-beijing', idc='ali'):
        self.idc = idc
        self.origin = origin
        self.region = region

    def client(self, c, name, idc):
        try:
            module = importlib.import_module(f'cjtmc_{name}.sdk.{idc}.{c}')
        except ModuleNotFoundError as e:
            raise FileClassNotFoundError()
        cls_str = str(c).capitalize()
        return getattr(module, cls_str)(**{'Origin': self.origin, 'RegionId': self.region})

    def converse_idc(self, idcname):
        return idcname if idcname not in ['dingding', 'jst', 'jushita'] else 'ali'

    def exec_func(self, clss, func, **kwargs):
        logger.info("执行{}文件的{}函数，具体参数为{}".format(clss, func, kwargs))
        name = 'base' if clss == 'regions' else clss
        cls = self.client(clss, name, self.converse_idc(self.idc))
        if hasattr(cls, func):
            return getattr(cls, func)(**kwargs)
        else:
            raise ModuleNotFoundError()
    # f = AllBase('dsada', 'cn-beijing', 'ali').exec_func('rds', 'start_ecs', **{})
    # print(f)
