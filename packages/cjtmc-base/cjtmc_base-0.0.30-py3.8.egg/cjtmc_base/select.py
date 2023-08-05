#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 11:53
# @Author  : Derek
# @Version : V0.1
# @function:
DBICTSelect = (
    ('Prepaid', '包年包月'),
    ('Postpaid', '按量付费')
)

DBIT = (
    ('Primary', '主实例'),
    ('ReadOnly', '只读实例'),
    ('Guard', '灾备实例'),
    ('Temp', '临时实例'),
)
DBCM = (
    ('Standard', '标准访问模式'),
    ('Performance', '数据库代理模式')
)
DBCate = (
    ('Basic', '基础版'),
    ('HighAvailability', '高可用版'),
    ('Finance', '金融版')
)
ICTSelect = (
    ('PrePaid', '包年包月'),
    ('PostPaid', '按量付费')
)

INCTSelect = (
    ('PayByBandwidth', '按带宽计费'),
    ('PayByTraffic', '按流量计费')
)
CategorySelect = (
    ('cloud', '普通云盘'),
    ('cloud_efficiency', '高效云盘'),
    ('cloud_ssd', 'SSD盘'),
    ('cloud_essd', 'ESSD云盘'),
    ('local_ssd_pro', 'I/O密集型本地盘'),
    ('local_hdd_pro', '吞吐密集型本地盘'),
    ('ephemeral', '本地盘'),
    ('ephemeral_ssd', '本地SSD盘'),
    ('SSD', '超高IO云硬盘'),
    ('GPSSD', '通用型云硬盘'),
    ('SAS', '高IO云硬盘'),
    ('SATA', '普通IO云硬盘'),
    ('CLOUD_BASIC', '普通云盘'),
    ('CLOUD_PREMIUM', '高性能云硬盘'),
    ('CLOUD_SSD', 'SSD云硬盘'),
    ('CLOUD_HSSD', '增强型SSD云硬盘'),
    ('CLOUD_TSSD', '极速型SSD云硬盘'),
)
StoppendMode = (('KeepCharging', "停机后继续收费"), ('StopCharging', "停机后不收费"), ('Not-applicable', '不支持'))

type_choices = (('cve', 'Linux漏洞'), ('sys', 'Windows漏洞'), ('cms', 'WebCMS漏洞'), ('emg', '应急漏洞'), ('app', '应用漏洞'))
status_choices = (
    ('1', "未修复"), ('2', '修复失败'), ('3', '回滚失败'), ('4', '修复中'), ('5', '回滚中'), ('6', '验证中'), ('7', '修复成功'),
    ('8', '修复成功待重启'), ('9', '回滚成功'), ('10', '已忽略'), ('11', '回滚成功待重启'), ('12', '漏洞不存在'), ('20', '已失效'))
necessity_choices = (('asap', '高'), ('later', '中'), ('nntf', '低'))
level_choices = (('serious', '紧急'), ('suspicious', '可疑'), ('remind', '提醒'))
