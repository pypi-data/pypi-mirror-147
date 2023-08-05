import logging

from cjtmc_base.models import Region
from cjtmc_base.sdk.openstack.base import OpenstackBase

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class Regions(OpenstackBase):
    def get_region(self):
        logger.info("----同步OpenStack可用区域开始----")
        Region.objects.update_or_create(
            defaults={'RegionId': "openstack", 'LocalName': "openstack", 'OriginId': self.Origin},
            OriginId=self.Origin,
            RegionId="openstack"
        )
        logger.info("----同步OpenStack可用区域结束----")
