#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 19:22
# @Author  : Derek
# @Version : V0.1
# @function:
from setuptools import setup, find_packages

setup(
    name="cjtmc-base",
    version="0.0.30",
    keywords=["pip", "chanjet_multicloud", "chanjet", "cjtmsp"],
    description="chanjetmulticloud-base sdk",
    long_description="chanjetmulticloud-base sdk for python",
    license="MIT Licence",
    dependency_links=[
        'https://pypi.douban.com/simple',
    ],
    url="https://www.cjtmsp.com",
    author="derek",
    author_email="wangshengh@chanjet.com",

    packages=find_packages(exclude=[
        'ez_setup', 't', 't.*',
    ]),
    include_package_data=True,
    platforms="any",
    zip_safe=False,
    install_requires=[
        "aliyun-python-sdk-core",
        "arrow",
        "celery",
        "huaweicloudsdkcore",
        "huaweicloudsdkiam",
        "mysqlclient",
        "pycryptodome",
        "python-keystoneclient",
        "tencentcloud-sdk-python",
        "djangorestframework",
        "django_celery_beat",
        "Ipy",
    ]
)
