# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/11/30 10:14
# @Author  : derek
# @File    : region.py
# @Version : 1.0
# 说明:
import logging

from cjtmc_base.models import Region
from cjtmc_base.sdk.vmware.base import VmwareBase

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class Regions(VmwareBase):
    def get_region(self):
        logger.info("----同步vmware可用区域开始----")
        Region.objects.update_or_create(defaults={'RegionId': "vmware", 'LocalName': "vmware", 'OriginId': self.Origin},
                                        RegionId="vmware"
                                        )
        logger.info("----同步vmware可用区域结束----")
