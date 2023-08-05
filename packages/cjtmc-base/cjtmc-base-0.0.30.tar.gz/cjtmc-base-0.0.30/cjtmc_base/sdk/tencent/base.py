# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/10/29 08:55
# @Author  : derek
# @File    : base.py
# @Version : 1.0
# 说明:

import logging
import math

from tencentcloud.billing.v20180709.billing_client import BillingClient
from tencentcloud.cbs.v20170312.cbs_client import CbsClient
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.cvm.v20170312.cvm_client import CvmClient
from tencentcloud.vpc.v20170312.vpc_client import *

from cjtmc_base.utils.rsa import decrypt

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class TencentBase(object):
    def __init__(self, *args, **kwargs) -> object:
        """
        出现异常：[TencentCloudSDKException] code:ClientNetworkError message:[SSL: CERTIFICATE_VERIFicate verify failed:
                unable to get local issuer certificate (_ssl.c:1124) requestId:None
        如何解决：/Applications/Python*/Install Certificates.command 或者 pip install --upgrade certifi
        """
        self.Origin = kwargs.get('Origin')
        self.AccessKeyId = kwargs.get('Origin').AccessKeyId
        self.AccessSecret = decrypt(kwargs.get('Origin').AccessSecret)
        self.RegionId = kwargs.get('RegionId')
        self.cred = credential.Credential(self.AccessKeyId, self.AccessSecret)

    def get_base(self, modelreq, params=None, endpoint='ecs', clinetreq=None):
        """
        通过分页的方式获取分页信息(默认每页100条数据),
        """
        if params is None: params = {}
        self.config(endpoint)
        # logger.info(f'分页获取tencent数据, params={params}')
        req = modelreq()
        if endpoint == 'billing':
            params.update({"Limit": 100, 'Offset': 0})
        else:
            params.update({"limit": 100, 'offset': 0})
        req.from_json_string(json.dumps(params))
        resp = getattr(self.client, clinetreq)(req)
        res = json.loads(resp.to_json_string())
        if 'TotalCount' in res:
            count = res['TotalCount']
        else:
            count = 100
        for page in range(0, math.ceil(count / 100) + 1):
            if endpoint == 'billing':
                params.update({"Limit": 100, 'Offset': page * 100})
            else:
                params.update({"limit": 100, 'offset': page * 100})
            req.from_json_string(json.dumps(params))
            resp = getattr(self.client, clinetreq)(req)
            response = json.loads(resp.to_json_string())
            logger.info("----数据返回，返回结果为{},账号为{}----".format(response, self.AccessKeyId))
            yield response

    def edit_base(self, endpoint='ecs', modelname=None, fname=None, params=None):
        """tencent执行函数的封装,eg:start,stop.reboot..."""
        if not params: params = {}
        self.config(endpoint=endpoint)
        request = modelname()
        request.from_json_string(json.dumps(params))
        fun = getattr(self.client, fname)
        try:
            response = self.new_response(fun(request))
        except Exception as e:
            logger.error(f'腾讯云{self.AccessKeyId}执行{fname}失败,原因:{str(e)}')
            return {'code': 500, 'message': f'执行失败,原因:{str(e)}', 'data': []}
        else:
            return {'code': 200, 'message': response, 'data': response}

    def get_field_name(self, model):
        """
        获取model的字段名称用于校验
        :param model:
        :return:
        """
        return [field.name for field in model._meta.get_fields() if field.name != 'id']

    def clientvcs(self, endpoint=None):
        return getattr(self, f'{endpoint}client')

    def config(self, endpoint=None):
        """添加配置, eg:endpoint=cvm"""
        endpoint2 = endpoint if endpoint != 'region' else 'cvm'
        e = "{}.tencentcloudapi.com".format(endpoint2)  # cvm.tencentcloudapi.com
        self.httpProfile = HttpProfile(endpoint=e, reqTimeout=30)  # 实例化一个 http 选项，可选的，没有特殊需求可以跳过。
        self.clientProfile = ClientProfile(httpProfile=self.httpProfile)  # 实例化一个 client 选项，可选的，没有特殊需求可以跳过。
        self.client = self.clientvcs(endpoint)

    @staticmethod
    def new_response(response):
        """默认返回响应信息为对象,进一步处理返回字典类型"""
        return json.loads(response.to_json_string())

    @property
    def vpcclient(self):
        client = VpcClient(self.cred, self.RegionId, self.clientProfile)
        return client

    @property
    def cbsclient(self):
        client = CbsClient(self.cred, self.RegionId, self.clientProfile)
        return client

    @property
    def cvmclient(self):
        client = CvmClient(self.cred, self.RegionId, self.clientProfile)
        return client

    @property
    def costclient(self):
        client = BillingClient(self.cred, self.RegionId, self.clientProfile)
        return client

    @property
    def regionclient(self):
        client = CvmClient(self.cred, "", self.clientProfile)
        return client

    @property
    def billingclient(self):
        client = BillingClient(self.cred, "", self.clientProfile)
        return client
