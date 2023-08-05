import logging
from uuid import uuid4

import requests
from django.conf import settings

from cjtmc_base.utils.rsa import decrypt

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class ZstackBase(object):
    byte2G = lambda self, x: int(x / 1024 / 1024 / 1024)
    uuid = property(fget=lambda x: "".join(str(uuid4()).split("-")))

    def __init__(self, *args, **kwargs):
        self.Origin = kwargs.get("Origin")
        self.name = self.Origin.AccessKeyId
        self.password = decrypt(self.Origin.AccessSecret)
        self.region = kwargs.get("RegionId", "zone-1")
        host, port = self.Origin.Settings.get("Ip"), self.Origin.Settings.get("Port")
        self.base_url = f"http://{host}:{port}"

    def login(self):
        """
        登录:获取一个Session UUID，以供后续API调用使用
        """
        login_data = {"logInByAccount": {"password": self.password, "accountName": self.name}}
        res = requests.post(self.base_url + "/zstack/v1/accounts/login", json=login_data).json()
        return res.get("inventory", {}).get("uuid")

    def logout(self, uuid):
        """
        登出:否则会报错(登录会话数量已经达到最大值)
        """
        return requests.post(self.base_url + f"/zstack/v1/accounts/sessions/{uuid}").json()

    def execute(self, url, data={}, method="get", web_hook=False):
        """
        执行zstack请求的核心代码
        :param url: 网址
        :param data: 数据
        :param method: 执行方法
        :param web_hook: 是否异步回调
        :return: 响应数据，字典
        """
        # logger.info(f"zstack base req=", url, data, method, web_hook)
        # 登录
        uuid = self.login()
        if not getattr(settings, 'ZSTACK_CALLBACK', ''):
            logger.error('请在配置文件中配置ZSTACK_CALLBACK回调网址')
            settings.ZSTACK_CALLBACK = 'http://www.xxx.com/api/callback/'
        # 核心操作
        extend_headers = {"X-Job-UUID": self.uuid, "X-Web-Hook": settings.ZSTACK_CALLBACK}
        headers = {"Authorization": "OAuth {}".format(uuid), "Content-Type": "application/json"}
        if web_hook: headers.update(**extend_headers)
        if method == "get":
            response = requests.get(url=self.base_url + url, headers=headers, params=data).json()
        else:
            response = requests.request(url=self.base_url + url, headers=headers, json=data, method=method).json()
        # 登出
        self.logout(uuid)
        return response

    def edit_base(self, url, data, method="post", web_hook=False):
        """
        执行功能封装
        """
        try:
            res = self.execute(url, data, method, web_hook)
        except Exception as e:
            response = {"code": 500, "msg": str(e), "data": []}
        else:
            response = {"code": 200, "msg": "执行成功", "data": res.get('inventory')}
        return response

    def get_base(self, url, data=None, pageSize=100):
        """
        获取功能封装(分页采集,默认每页100条)
        """
        if not data: data = {"start": 0, "limit": pageSize, "replyWithCount": True}
        # 数据总数，用于确定分页
        total = self.execute(url, data, "get").get("total", 0)

        pages = int(total // pageSize) + 1
        for page in range(pages):
            logger.info(f"page={page},url={url}采集数据")
            data["start"] = page * pageSize
            results = self.execute(url, data, 'get').get("inventories", {})
            yield from results
