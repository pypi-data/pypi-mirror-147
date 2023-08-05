#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/24 10:53
# @Author  : Derek
# @Version : V0.1
# @function:
import logging

from celery import shared_task

from cjtmc_base.api.all import AllBase
from cjtmc_base.models import IDC, Origin

logger = logging.getLogger('chanjetmulticloud_base.utils.log.tasks')


def converse_idc(idcname):
    if idcname in ['dingding', 'jst', 'jushita']:
        return 'ali'
    return idcname


@shared_task()
def get_all_regions():
    """采集所有主机的region信息"""
    for idc in IDC.objects.all():
        orgid = Origin.objects.filter(IDC=idc).all()
        for o in orgid:
            logger.info(f'get_all_regions: {idc.Idc}-{o}')
            try:
                idcname = converse_idc(idc.Name)
                AllBase(o, 'cn-beijing', idcname).exec_func('regions', 'get_region')
            except Exception as e:
                logger.error(f'get_all_regions: {idc.Idc}-{o} 采集失败, 原因:{str(e)}')


@shared_task()
def get_all_base(idc, model, cls, region='all', params=None, ak=None):
    """
    封装的函数,支持指定ak和指定region的函数执行
    ak = ['xxx', 'xxxx']
    region = 'cn-beijing'
    """
    if not params: params = {}
    if not ak: ak = []
    orgids = Origin.objects.filter(IDC__Name=idc)
    if ak:
        orgids = orgids.filter(AccessKeyId__in=ak)
    for o in orgids:
        regions = o.region_set.all() if region == 'all' else o.region_set.filter(RegionId=region)
        for r in regions:
            # 不要删, 如果异常，不影响后续的函数执行
            try:
                idc = converse_idc(idc)  # 兼容钉钉云和聚石塔使用ali的sdk接口。
                AllBase(o, r.RegionId, idc).exec_func(cls, model, **params)
            except Exception as e:
                logger.error(f'idc={idc},origin={o} execute {model} failed, reason={str(e)}')
