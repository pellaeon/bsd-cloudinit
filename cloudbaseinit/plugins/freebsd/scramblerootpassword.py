# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Pellaeon Lin <pellaeon@hs.ntnu.edu.tw>
#
#    Licensed under the Apache License, Version 2.0 (the 'License'); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cloudbaseinit.openstack.common import log as logging
from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins.common import base

LOG = logging.getLogger(__name__)

class ScrambleRootPassword(base.BasePlugin):
    def _get_password(self, osutils):
        # Generate a temporary random password to be replaced
        # by SetUserPasswordPlugin (starting from Grizzly)
        return osutils.generate_random_password(14)

    def execute(self, service, shared_data):
        osutils = osutils_factory.get_os_utils()
        password = self._get_password(osutils)

        LOG.info('Scrambling root password')
        osutils.set_user_password('root', password)

        return (base.PLUGIN_EXECUTION_DONE, False)
