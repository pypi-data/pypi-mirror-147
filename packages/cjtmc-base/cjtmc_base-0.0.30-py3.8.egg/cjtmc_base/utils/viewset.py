#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/9 20:28
# @Author  : Derek
# @Version : V0.1
# @function:
from collections import OrderedDict

from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework.viewsets import ModelViewSet


class PageNumber(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'  # URL中每页显示条数的参数
    page_query_param = 'pageNumber'  # URL中页码的参数
    max_page_size = None  # 最大页码数限制

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('list', data),
        ]))


class CustomModelViewSet(ModelViewSet):
    """重写ModelViewSet确保返回信息为{'code': xxx, 'msg': '成功', 'errors': {}, 'data': []} """
    pagination_class = PageNumber

    def create(self, request, *args, **kwargs):
        print(self.request.query_params)
        response = super(CustomModelViewSet, self).create(request, *args, **kwargs)
        return Response({'code': 200, "message": "创建成功", "data": response.data})

    def retrieve(self, request, *args, **kwargs):
        response = super(CustomModelViewSet, self).retrieve(request, *args, **kwargs)
        # response.data, headers=response.status_code
        return Response({"message": "查看详情成功", "code": 200, "data": response.data})

    def update(self, request, *args, **kwargs):
        response = super(CustomModelViewSet, self).update(request, *args, **kwargs)
        return Response({'code': 200, "message": "更新成功", "data": response.data})

    def destroy(self, request, *args, **kwargs):
        response = super(CustomModelViewSet, self).destroy(request, *args, **kwargs)
        return Response({'code': 200, "message": "删除成功", "data": response.data})

    def list(self, request, *args, **kwargs):
        response = super(CustomModelViewSet, self).list(request, *args, **kwargs)
        return Response({'code': 200, "message": "查看成功", "data": response.data})


# 异常处理机制
def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = exc.detail
        set_rollback()
        return Response({'code': 500, "msg": '失败原因:' + str(data), "errors": data, 'data': []},
                        status=exc.status_code,
                        headers=headers)
    return None
