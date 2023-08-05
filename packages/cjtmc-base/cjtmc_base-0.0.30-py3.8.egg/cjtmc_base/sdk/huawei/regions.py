# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/10/29 10:30
# @Author  : derek
# @File    : regions.py
# @Version : 1.0
# 说明:
import logging

from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkiam.v3 import IamClient, KeystoneListProjectsRequest

from cjtmc_base.models import Region
from cjtmc_base.sdk.huawei.base import HuaweiBase

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class Regions(HuaweiBase):

    def get_region(self, *args, **kwargs):
        endpoint = "https://iam.myhuaweicloud.com"
        config = HttpConfig.get_default_config()
        config.timeout = 3
        config.ignore_ssl_verification = True
        credentials = GlobalCredentials(self.AccessKeyId, self.AccessSecret)

        client = IamClient.new_builder(IamClient).with_http_config(config). \
            with_credentials(credentials). \
            with_endpoint(endpoint).build()

        request = KeystoneListProjectsRequest()
        try:
            projects = client.keystone_list_projects(request)
        except Exception as e:
            return False
        project_dict = {
            'cn-northeast-1': "东北-大连",
            'cn-north-4': '华北-北京四',
            "cn-north-1": "华北-北京一",
            'cn-east-2': '华东-上海二',
            'cn-east-3': '华东-上海一',
            'cn-south-1': '华南-广州',
            'af-south-1': '南非-约翰内斯堡',
            'eu-west-0': '欧洲-巴黎',
            'ap-southeast-1': '亚太-香港',
            'ap-southeast-3': '亚太-新加坡',
            'cn-southwest-2': '西南-贵阳一',
            'ap-southeast-2': '亚太-曼谷'
        }

        logger.info("-----数据为{}----".format(projects))
        for project in projects.projects:
            project = project.to_dict()
            if project.get("name") != 'MOS':
                Region.objects.get_or_create(RegionId=project.get("name"), RegionEndpoint=project.get("id"),
                                             OriginId=self.Origin,
                                             LocalName=project_dict.get(project.get("name"), project.get("name")))
