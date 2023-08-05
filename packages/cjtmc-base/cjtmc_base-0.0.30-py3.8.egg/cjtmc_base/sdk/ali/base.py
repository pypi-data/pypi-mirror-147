import json
import logging
import math
import random
import time

from aliyunsdkcore.client import AcsClient

from cjtmc_base.utils.rsa import decrypt

logger = logging.getLogger('cjtmc_base.utils.log.tasks')


class AliBase():

    def __init__(self, Origin=None, RegionId='cn-hangzhou'):
        self.Origin = Origin
        self.AccessKeyId = Origin.AccessKeyId
        self.AccessSecret = decrypt(Origin.AccessSecret)
        self.RegionId = RegionId
        self.client = AcsClient(self.AccessKeyId, self.AccessSecret, self.RegionId, timeout=100)

    def get_filed_name(self, model):
        """
        获取model的字段名称用于校验
        :param model:
        :return:
        """
        return [field.name for field in model._meta.get_fields() if field.name != 'id']

    def edit_base(self, modelname=None, param={}):
        request = modelname()
        request.set_accept_format('json')
        for k, v in param.items():
            request.add_query_param(k, str(v).strip())
        logger.info("模块为{},参数为{}".format(modelname, request.get_query_params()))
        response = self.get_response(request)
        return response

    def get_base(self, modelname=None, param=None):
        """
        通过分页的方式获取分页信息
        """
        if param is None: param = {}
        request = modelname()
        request.set_accept_format('json')
        request.add_query_param('PageSize', 50)
        request.add_query_param('CurrentPage', 1)
        for p, v in param.items():
            request.add_query_param(p, str(v).strip())
        response = self.get_response(request).get('message')
        pagenum = "PageNumber"
        if 'TotalCount' in response:
            count = response['TotalCount']
        # 不要删,采集Arms需要定制的页参数
        elif 'PageBean' in response and modelname.__name__ in ("SearchAlertRulesRequest"):
            count = response.get('PageBean').get('TotalCount')
            pagenum = "CurrentPage"
        elif 'TotalRecordCount' in response:
            count = response.get('TotalRecordCount')
        elif 'TotalItems' in response:
            count = response.get('TotalItems')
        elif 'PageBean' in response:
            count = response.get('PageBean').get('TotalCount')
        elif 'Data' in response and modelname.__name__ in (
                "QueryInstanceBillRequest", "DescribeSplitItemBillRequest", "QueryCostUnitRequest",
                "QueryCostUnitResourceRequest"):  # 获取账单数据的多嵌套了一层，所以需要get 2次
            count = response.get("Data").get("TotalCount")
            pagenum = "PageNum"
        elif modelname.__name__ in ('DescribeAlarmEventListRequest'):
            pagenum = "CurrentPage"
            count = response.get('PageInfo').get('TotalCount')
        else:
            count = 100
        for page in range(1, math.ceil(count / 50) + 1):
            request.add_query_param(pagenum, page)
            response = self.get_response(request)
            yield response.get('message', {})

    def get_base_by_token(self, modelname=None, param=None) -> dict:
        """
        通过token方式分页获取信息
        """
        if not param: param = {}
        request = modelname()
        request.set_accept_format('json')
        request.add_query_param('MaxResults', 50)  # 每页条数
        for p, v in param.items():
            # 这里p是执行方法，查看阿里云sdk源码发现，"set_方法名"到了这里就得变成 "方法名",举个例子，查询账单是request.set_BillingCycle，到了这里就得写成 BillingCycle
            request.add_query_param(p, str(v).strip())
        response = self.get_response(request)
        # response.get('NextToken')是云主机、磁盘信息等获取token的方式
        # response.get("Data", {}).get('NextToken')是分账账单获取token的方式
        # 如果有特殊情况，自行在后面添加token获取方式
        token = response.get('message').get('NextToken') or response.get('message').get("Data", {}).get('NextToken')
        yield response.get('message', {})
        while token:
            request.add_query_param('MaxResults', 50)  # 每页条数
            for p, v in param.items():
                # 这里p是执行方法，查看阿里云sdk源码发现，"set_方法名"到了这里就得变成 "方法名",举个例子，查询账单是request.set_BillingCycle，到了这里就得写成 BillingCycle
                request.add_query_param(p, str(v).strip())
            request.add_query_param("NextToken", token)
            response = self.get_response(request)
            token = response.get('message').get('NextToken') or response.get('message').get("Data", {}).get('NextToken')
            yield response.get('message', {})

    def get_response(self, request):
        """根据请求返回处理后的响应信息"""
        try:
            response = {'code': 200,
                        'message': json.loads(self.client.do_action_with_exception(request).decode('utf-8'))}
        except Exception as e:
            response = {'code': 500, 'message': str(e)}
            logger.error('连接阿里云失败，错误代码为{}'.format(e))
            RETRY_MSGS = ['Throttling', 'LastTokenProcessing', 'SYSTEM.CONCURRENT_OPERATE']
            # 只要任意一个可以触发重试的信息在str(e)存在，则重试
            if any([retry_msg in str(e) for retry_msg in RETRY_MSGS]):
                time.sleep(random.randint(60, 60 * 5))
                logger.info('限流后重试....')
                response = {'code': 200,
                            'message': json.loads(self.client.do_action_with_exception(request).decode('utf-8'))
                            }

        return response
