#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 19:19
# @Author  : Derek
# @Version : V0.1
# @function:

class FileClassNotFoundError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return ('当前云平台没有此文件，不能进行操作')


class InstanceNotFoundError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return ('当前机器未找到，请重新查询')
