# !/usr/bin/env python
# coding: utf-8
# @Time    : 2020/7/27 14:48
# @Author  : derek
# @File    : serializer.py
# @Version : 1.0
# 说明:
from rest_framework import serializers

from cjtmc_base.models import Origin, IDC, Env


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        exclude = ['AccessSecret']
        depth = 2


class IdcSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = '__all__'


class EnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Env
        fields = '__all__'
