# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Cloudbase Solutions Srl
# Copyright 2014 Pellaeon Lin <pellaeon@hs.ntnu.edu.tw>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo.config import cfg

from cloudbaseinit.openstack.common import log as logging
from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins import base

CONF = cfg.CONF
CONF.register_opts(opts)

LOG = logging.getLogger(__name__)

class SetHostNamePlugin(base.BasePlugin):
    def execute(self, service, shared_data):
        osutils = osutils_factory.get_os_utils()

        metadata_host_name = service.get_host_name()
        if not metadata_host_name:
            LOG.debug('Hostname not found in metadata')

        # In FreeBSD, hostname means FQDN, so no split is needed
        osutils.set_host_name(metadata_host_name)

        return (base.PLUGIN_EXECUTION_DONE, False)
