from keystoneauth1.identity import v3
from keystoneauth1.session import Session

from cjtmc_base.models import Origin
from cjtmc_base.utils.rsa import decrypt


class OpenstackBase(object):
    def __init__(self, *args, **kwargs):
        default_origin = Origin.objects.filter(IDC__Idc="openstack").first()
        self.Origin = kwargs.get('Origin', default_origin)
        self.username = self.Origin.AccessKeyId
        self.password = decrypt(self.Origin.AccessSecret)
        self.region = kwargs.get('RegionId', 'Default')
        self.auth_url = self.Origin.Settings.get('AuthUrl')
        self.user_domain_name = self.Origin.Settings.get('UserDomainName')
        self.project_domain_name = self.Origin.Settings.get('UserProjectId')

    @property
    def auth(self):
        auth = v3.Password(username=self.username,
                           password=self.password,
                           user_domain_name=self.user_domain_name,
                           project_domain_name=self.project_domain_name,
                           auth_url=self.auth_url)
        return Session(auth=auth)

    def edit_base(self, modelname=None, param=None):
        """
        执行功能封装
        """
        pass

    def get_base(self, modelname=None, param=None):
        """
        获取功能封装
        """
        pass
