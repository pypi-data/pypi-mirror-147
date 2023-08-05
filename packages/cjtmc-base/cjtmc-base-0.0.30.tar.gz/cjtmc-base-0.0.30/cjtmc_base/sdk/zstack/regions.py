import logging

from cjtmc_base.models import Region
from cjtmc_base.sdk.zstack.base import ZstackBase

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class Regions(ZstackBase):
    def get_region(self):
        try:
            logger.info("----同步Zstack可用区域开始----")
            for zone in self.get_base(url='/zstack/v1/zones'):
                data = {'RegionId': zone.get('name').lower(), 'LocalName': zone.get('name').lower(), 'Sync': True,
                        'OriginId': self.Origin}
                Region.objects.update_or_create(
                    defaults=data, OriginId=self.Origin, RegionId=zone.get('name').lower())
            logger.info("----同步Zstack可用区域结束----")
            return True
        except Exception as e:
            return False

# python try except exception django pandas requests response vmware openstack
# byte isdigit ZeroDivisionError Traceback
