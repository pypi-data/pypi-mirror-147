from django.db import models


class BaseModel(models.Model):
    CreateTime = models.DateTimeField('创建时间', auto_now_add=True, )
    ChangeTime = models.DateTimeField('修改时间', auto_now=True)
    Sync = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ("-CreateTime",)


# Create your models here.
class IDC(models.Model):
    Name = models.CharField('名称', max_length=100, blank=True, null=True)
    Idc = models.CharField('简称', max_length=100, blank=True, null=True)
    Default = models.CharField('默认区域', max_length=100, blank=True, null=True, default='cn-beijing')
    Remark = models.CharField('备注信息', max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s-%s" % (self.Name, self.Idc)


class Origin(BaseModel):
    """
    存放认证信息
    """
    IDC = models.ForeignKey(IDC, on_delete=models.CASCADE, related_name="idc")
    Name = models.CharField('Name', max_length=100, blank=True, null=True, db_index=True)
    AccessKeyId = models.CharField('access Key Id', max_length=100, blank=True, null=True)
    AccessSecret = models.CharField('access Secret', max_length=1000, blank=True, null=True)
    Remark = models.CharField('备注信息', max_length=100, blank=True, null=True)
    Settings = models.JSONField(verbose_name='其他配置信息')
    Default = models.BooleanField('是否为默认账号', default=False)


class Region(BaseModel):
    """
    接入地址
    """
    RegionId = models.CharField('位置', max_length=100, blank=True, null=True, db_index=True)
    RegionEndpoint = models.CharField('地域对应的接入地址', max_length=100, blank=True, null=True)
    LocalName = models.CharField('地域名称', max_length=100, blank=True, null=True)
    OriginId = models.ForeignKey(Origin, on_delete=models.CASCADE, blank=True, null=True, db_index=True)

    def __str__(self):
        return "{}的{}区域".format(self.OriginId.AccessKeyId, self.LocalName)


class Env(BaseModel):
    Name = models.CharField('名字', max_length=100, blank=True, null=True)
    Code = models.CharField("英文标识", max_length=100, blank=True, null=True, unique=True)
    Status = models.BooleanField('环境是否可用', default=1)
    Priority = models.IntegerField('显示优先级', default=0, help_text='优先级递增(0-10)')
    SiteId = models.IntegerField('租户id', blank=True, null=True, default=1)

    class Meta:
        verbose_name = '环境数据表'
        ordering = ('-Priority', 'Name')
