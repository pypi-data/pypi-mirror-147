# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/10/19 08:59
# @Author  : derek
# @File    : regions.py
# @Version : 1.0
# 说明:
import logging

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312.models import DescribeRegionsRequest

from cjtmc_base.models import Region
from cjtmc_base.sdk.tencent.base import TencentBase

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class Regions(TencentBase):

    def get_region(self):
        """
        获取region
        :return:
        """
        logger.info("----同步腾讯云可用区域开始----")
        try:
            for regions in self.get_base(DescribeRegionsRequest, {}, 'region', 'DescribeRegions'):
                for region in regions.get('RegionSet', []):
                    data_region = {'RegionId': region.get('Region'),
                                   'LocalName': region.get('RegionName'),
                                   'OriginId': self.Origin}
                    Region.objects.update_or_create(defaults=data_region, LocalName=region.get('RegionName'))
        except TencentCloudSDKException as err:
            logger.error("----同步腾讯云可用区域失败,失败原因为{}----".format(err))
        logger.info("----同步腾讯云可用区域结束----")
