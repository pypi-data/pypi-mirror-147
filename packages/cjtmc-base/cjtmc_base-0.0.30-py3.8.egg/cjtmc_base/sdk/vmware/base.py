import atexit
import logging

import requests
import urllib3
from com.vmware.vcenter_client import VM, Datacenter, ResourcePool, Folder, Datastore, Network
from pyVim.connect import Disconnect
from pyVim.connect import SmartConnect
from vmware.vapi.vsphere.client import create_vsphere_client

from cjtmc_base.models import Origin
from cjtmc_base.utils.rsa import decrypt

logger = logging.getLogger("cjtmc_base.utils.log.tasks")


class VmwareBase():
    def __init__(self, *args, **kwargs):
        default_origin = Origin.objects.filter(IDC__Idc='vmware').first()
        self.Origin = kwargs.get('Origin', default_origin)
        session = requests.session()
        session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        host = self.Origin.Settings.get('server')
        username = self.Origin.AccessKeyId
        password = decrypt(self.Origin.AccessSecret)
        self.client = create_vsphere_client(server=host, username=username, password=password, session=session)
        self.si = self.connect(host=host, user=username, password=password)
        self.content = self.si.RetrieveContent()

    def connect(self, host, user, password, disable_ssl_verification=True):
        """
        Determine the most preferred API version supported by the specified server,
        then connect to the specified server using that API version, login and return
        the service instance object.
        """
        service_instance = None
        conn_params = dict(host=host, user=user, pwd=password)
        # form a connection...
        try:
            if disable_ssl_verification:
                conn_params['disableSslCertValidation'] = True
                service_instance = SmartConnect(**conn_params)
            else:
                service_instance = SmartConnect(**conn_params)
            # doing this means you don't need to remember to disconnect your script/objects
            atexit.register(Disconnect, service_instance)
        except IOError as io_error:
            logger.error(io_error)
        if not service_instance:
            raise SystemExit("Unable to connect to host with supplied credentials.")
        return service_instance

    @property
    def vmclient(self):
        return self.client.vcenter.VM

    @property
    def powerclient(self):
        return self.client.vcenter.vm.Power

    @property
    def vpclient(self):
        return self.client.vcenter.Network

    @property
    def resourcepool_client(self):
        return self.client.vcenter.ResourcePool

    @property
    def folder_client(self):
        return self.client.vcenter.Folder

    @property
    def niclient(self):
        return self.client.vcenter.vm.hardware.Ethernet

    def get_datacenter(self, datacenter_name):
        filter_spec = Datacenter.FilterSpec(names={datacenter_name})
        datacenter_summaries = self.client.vcenter.Datacenter.list(filter_spec)
        if len(datacenter_summaries) > 0:
            datacenter = datacenter_summaries[0].datacenter
            return datacenter
        else:
            return None

    def get_resource_pool(self, datacenter_name, resource_pool_name=None):
        """
        根据资源池名称返回资源池对象，如果resource_pool_name不存在，则返回该datacenter的第一个资源池对象。
        """
        datacenter = self.get_datacenter(datacenter_name)
        if not datacenter:
            logger.info("Datacenter '{}' not found".format(datacenter_name))
            return None
        names = {resource_pool_name} if resource_pool_name else None
        filter_spec = ResourcePool.FilterSpec(datacenters={datacenter}, names=names)
        resource_pool_summaries = self.resourcepool_client.list(filter_spec)
        if len(resource_pool_summaries) > 0:
            resource_pool = resource_pool_summaries[0].resource_pool
            logger.info("Selecting ResourcePool '{}'".format(resource_pool))
            return resource_pool
        else:
            logger.info("ResourcePool not found in Datacenter '{}'".
                        format(datacenter_name))
            return None

    def get_folder(self, datacenter_name, folder_name):
        datacenter = self.get_datacenter(datacenter_name)
        if not datacenter:
            logger.info("Datacenter '{}' not found".format(datacenter_name))
            return None

        filter_spec = Folder.FilterSpec(type=Folder.Type.VIRTUAL_MACHINE,
                                        names={folder_name},
                                        datacenters={datacenter})

        folder_summaries = self.folder_client.list(filter_spec)
        if len(folder_summaries) > 0:
            folder = folder_summaries[0].folder
            logger.info("Detected folder '{}' as {}".format(folder_name, folder))
            return folder
        else:
            logger.info("Folder '{}' not found".format(folder_name))
            return None

    def get_datastore(self, datacenter_name, datastore_name):
        datacenter = self.get_datacenter(datacenter_name)
        if not datacenter:
            logger.info("Datacenter '{}' not found".format(datacenter_name))
            return None

        filter_spec = Datastore.FilterSpec(names={datastore_name},
                                           datacenters={datacenter})

        datastore_summaries = self.client.vcenter.Datastore.list(filter_spec)
        if len(datastore_summaries) > 0:
            datastore = datastore_summaries[0].datastore
            logger.info("Detected datastore '{}' as {}".format(datacenter_name, datastore))
            return datastore
        else:
            return None

    def get_placement_spec(self, datacenter_name, vm_folder_name, datastore_name):
        """
        Returns a VM placement spec for a resourcepool. Ensures that the
        vm folder and datastore are all in the same datacenter which is specified.
        """
        resource_pool = self.get_resource_pool(datacenter_name)
        folder = self.get_folder(datacenter_name, vm_folder_name)
        datastore = self.get_datastore(datacenter_name, datastore_name)
        placement_spec = VM.PlacementSpec(folder=folder,
                                          resource_pool=resource_pool,
                                          datastore=datastore)
        logger.info("get_placement_spec_for_resource_pool: Result is '{}'".format(placement_spec))
        return placement_spec

    def get_network_backing(self, porggroup_name, datacenter_name, portgroup_type):
        """列出网络"""
        datacenter = self.get_datacenter(datacenter_name)
        if not datacenter:
            logger.info("Datacenter '{}' not found".format(datacenter_name))
            return None

        filter = Network.FilterSpec(datacenters={datacenter},
                                    names={porggroup_name},
                                    types={portgroup_type})
        network_summaries = self.vpclient.list(filter=filter)
        if len(network_summaries) > 0:
            network = network_summaries[0].network
            logger.info("Selecting {} Portgroup Network '{}' ({})".
                        format(portgroup_type, porggroup_name, network))
            return network
        else:
            logger.info("Portgroup Network not found in Datacenter '{}'".
                        format(datacenter_name))
            return None
