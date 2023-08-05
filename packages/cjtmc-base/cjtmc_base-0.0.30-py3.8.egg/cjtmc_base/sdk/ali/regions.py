# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/10/19 08:59
# @Author  : derek
# @File    : regions.py
# @Version : 1.0
# 说明:
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest

from cjtmc_base.models import Region
from cjtmc_base.sdk.ali.base import AliBase


class Regions(AliBase):

    def get_region(self):
        """
        获取region
        :return:
        """
        client = AcsClient(self.AccessKeyId, self.AccessSecret)
        request = DescribeRegionsRequest()
        request.set_accept_format('json')
        try:
            response = json.loads(client.do_action_with_exception(request).decode('utf-8'))
            for region in response.get('Regions').get('Region'):
                if region:
                    region['OriginId'] = self.Origin
                    Region.objects.get_or_create(**region)
            return True
        except Exception as e:
            return False
