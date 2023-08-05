# Create your views here.
import logging

from django.db.models import Q
from rest_framework.response import Response

from cjtmc_base.api.all import AllBase
from cjtmc_base.base.serializer import OriginSerializer, IdcSerializer, EnvSerializer
from cjtmc_base.models import Origin, IDC, Env
from cjtmc_base.utils.rsa import encrypt
from cjtmc_base.utils.viewset import CustomModelViewSet

logger = logging.getLogger('cjtmc_base.utils.log.tasks')


class OrginAPIView(CustomModelViewSet):
    """
    list:
    获取列表
    retrieve:
    获取其中一个详情
    update:
    修改
    delete:
    删除
    create:
    创建
    """
    serializer_class = OriginSerializer
    queryset = Origin.objects.all()

    def get_queryset(self):
        keyword = self.request.query_params.get('keyWord', '')
        origin = Origin.objects.all()
        if keyword:
            origin = origin.filter(AccessKeyId__icontains=keyword)
        idc = self.request.query_params.get('idc', '')
        if idc:
            origin = origin.filter(IDC__Name=keyword)
        return origin.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data["AccessSecret"] = encrypt(data['AccessSecret'])
        if data.get('IDC') == "openstack":
            data['Settings'] = {"AuthUrl": data.get("AuthUrl"), "UserDomainName": data.get("UserDomainName"),
                                "UserProjectId": data.get("UserProjectId")}
        elif data.get('IDC') == "zstack":
            data['Settings'] = {"Ip": data.get("Ip"), "Port": data.get("Port")}
        else:
            data['Settings'] = {}
        data['IDC'] = IDC.objects.filter(Name=data.get('IDC')).first()
        oid = Origin.objects.create(**data)
        try:
            AllBase(origin=oid, idc=data.get('Idc', 'ali')).exec_func('regions', 'get_region')
        except Exception as e:
            logger.exception(e)
            oid.delete()
            return Response({"code": 10001, "message": "添加失败，原因:账号异常，无法采集信息.", })
        return Response({"code": 200, "message": "添加成功"})


class IdcViewSet(CustomModelViewSet):
    serializer_class = IdcSerializer

    def get_queryset(self):
        idc = IDC.objects.all()
        keyword = self.request.query_params.get('keyWord', '')
        if keyword:
            idc = idc.filter(Q(Idc__icontains=keyword) | Q(Name__icontains=keyword))
        return idc.all()


class EnvAPIView(CustomModelViewSet):
    serializer_class = EnvSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyWord', '')
        env = Env.objects.all()
        if keyword:
            env = env.filter(Code__icontains=keyword)
        status = self.request.query_params.get('status', '')
        if status:
            env = env.filter(Status=status)
        return env.all()
