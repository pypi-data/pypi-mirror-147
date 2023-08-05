#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/20 17:25
# @Author  : Derek
# @Version : V0.1
# @function:
from django.db.models.signals import post_migrate
from django_celery_beat.models import CrontabSchedule, PeriodicTask

# 定义receiver函数
from cjtmc_base.models import IDC


def init_idc(sender, **kwargs):
    if sender.name == 'cjtmc_base':
        datas = [{'Name': 'ali', "Idc": '阿里云', "Default": "cn-beijing"},
                 {'Name': 'huawei', "Idc": '华为云', "Default": "cn-north-4"},
                 {'Name': 'tencent', "Idc": '腾讯云', "Default": "cn-beijing"},
                 {'Name': 'openstack', "Idc": 'Openstack', "Default": "cn-beijing"},
                 {"Name": 'zstack', "Idc": 'Zstack', "Default": "cn-beijing"},
                 {"Name": 'ctyun', "Idc": '天翼云', "Default": "cn-beijing"},
                 {"Name": 'dingding', "Idc": '钉钉云', "Default": "cn-beijing"},
                 {"Name": 'jushita', "Idc": '聚石塔', "Default": "cn-beijing"},
                 {"Name": 'kunpeng', "Idc": '鲲鹏', "Default": "cn-beijing"},
                 {"Name": 'jd', "Idc": "京东云", "Default": "cn-beijing"},
                 {"Name": "baidu", "Idc": "百度云", "Default": "cn-beijing"},
                 {"Name": "ucloud", "Idc": "Ucloud", "Default": "cn-beijing"},
                 {"Name": "aws", "Idc": "AWS", "Default": "cn-beijing"},
                 {"Name": "azure", "Idc": "Azure", "Default": "cn-beijing"},
                 {"Name": "qingcloud", "Idc": "青云", "Default": "cn-beijing"},
                 {"Name": "ksyun", "Idc": "金山云", "Default": "cn-beijing"},
                 {"Name": "qiniu", "Idc": '七牛云', "Default": "cn-beijing"},
                 {"Name": "inspur", "Idc": "浪潮云", "Default": "cn-beijing"},
                 {"Name": "yisu", "Idc": "亿速云", "Default": "cn-beijing"},
                 {"Name": "google", "Idc": '谷歌云', "Default": "cn-beijing"},
                 {"Name": "ibm", "Idc": "IBM云", "Default": "cn-beijing"}
                 ]
        for item in datas:
            IDC.objects.update_or_create(defaults=item, Name=item.get("Name"), Idc=item.get("Idc"))
        print('初始化idc数据成功')


def init_task(sender, **kwargs):
    if sender.name == 'cjtmc_base':
        mid, status = CrontabSchedule.objects.get_or_create(minute="0", hour="1", day_of_week='*', day_of_month='1',
                                                            month_of_year='*', timezone='Asia/Shanghai')

        PeriodicTask.objects.get_or_create(name='get_all_regions',
                                           task='cjtmc_base.tasks.resources.get_all_regions',
                                           crontab=mid)
        print('初始化定时任务成功')


post_migrate.connect(init_idc)
post_migrate.connect(init_task)
