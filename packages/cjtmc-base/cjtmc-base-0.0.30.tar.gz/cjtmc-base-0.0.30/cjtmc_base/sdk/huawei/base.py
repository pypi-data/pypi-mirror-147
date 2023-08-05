# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/10/29 08:55
# @Author  : derek
# @File    : base.py
# @Version : 1.0
# 说明:

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig

from cjtmc_base.utils.rsa import decrypt


class HuaweiBase():

    def __init__(self, Origin=None, RegionId='cn-north-4'):
        self.Origin = Origin
        self.AccessKeyId = Origin.AccessKeyId
        self.AccessSecret = decrypt(Origin.AccessSecret)
        self.region = RegionId  # cn-north-4
        self.RegionId = str("_".join(RegionId.split("-"))).upper() if RegionId else ""  # CN_NORTH_4
        print(self.Origin, self.AccessKeyId)

    def get_filed_name(self, model):
        """
        获取model的字段名称用于校验
        :param model:
        :return:
        """
        return [field.name for field in model._meta.get_fields() if field.name != 'id']

    @property
    def config(self):
        config = HttpConfig.get_default_config()
        config.timeout = 100
        config.ignore_ssl_verification = True
        return config

    @property
    def basecredentials(self):
        return BasicCredentials(self.AccessKeyId, self.AccessSecret)

    @property
    def globalcredentials(self):
        return GlobalCredentials(self.AccessKeyId, self.AccessSecret)


from functools import wraps
import logging

logger = logging.getLogger("tasks")


def edit_base(fun):
    """用于统一返回值，如果失败返回500状态码"""

    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            msg = fun(*args, **kwargs)
            response = {'code': 200, 'message': '执行成功', 'data': str(msg)}
        except Exception as e:
            logger.error('连接云sdk失败，错误代码为{}'.format(e))
            response = {'code': 500, 'message': str(e)}  # e转成字符串，便于返回报错信息
        return response

    return wrapper
