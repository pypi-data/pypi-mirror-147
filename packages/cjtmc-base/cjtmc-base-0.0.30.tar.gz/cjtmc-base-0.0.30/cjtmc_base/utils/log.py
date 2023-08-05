#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/15 15:01
# @Author  : Derek
# @Version : V0.1
# @function:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'filters': {
        'require_debug_true': {  # 只有在setting中的 DEBUG = True 的时候才会生效
            '()': 'django.utils.log.RequireDebugTrue',
        }, },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'utils.log_handler.MultiCompatibleTimedRotatingFileHandler',
            'filename': '/var/log/multicloud/error.log',
            'when': 'MIDNIGHT',
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': ['require_debug_true']
        },
        'tasks_handler': {
            'level': 'DEBUG',
            'class': 'utils.log_handler.MultiCompatibleTimedRotatingFileHandler',
            'filename': '/var/log/multicloud/tasks.log',
            'when': 'MIDNIGHT',
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'tasks': {
            'handlers': ['tasks_handler', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
