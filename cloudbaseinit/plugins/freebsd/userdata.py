# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2016 Ganael Laplanche, OVH <ganael.laplanche@corp.ovh.com>
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

from cloudbaseinit.openstack.common import log as logging
from cloudbaseinit.plugins.common import base

from tempfile import mkstemp
import os
import stat
import subprocess

LOG = logging.getLogger(__name__)

class UserDataPlugin(base.BasePlugin):
    def execute(self, service, shared_data):
        # Retrieve user data
        userdata = service.get_user_data()
        if not userdata:
            LOG.debug('User data not found in metadata')
            return (base.PLUGIN_EXECUTION_DONE, False)

        # Generate temporary script
        try:
            userdata_fd, userdata_file = mkstemp(prefix=".bsd-cloudinit-")
        except:
            LOG.debug('Cannot create temporary user data file')
            return (base.PLUGIN_EXECUTION_DONE, False)

        if os.write(userdata_fd, userdata) < 0:
            os.close(userdata_fd)
            os.unlink(userdata_file)
            LOG.debug('Cannot store user data to temporary file')
            return (base.PLUGIN_EXECUTION_DONE, False)
        os.close(userdata_fd)
        os.chmod(userdata_file, stat.S_IRUSR | stat.S_IXUSR)

        # Execute it
        subprocess.check_call(userdata_file, shell=True)

        # Clean-up
        os.unlink(userdata_file)

        return (base.PLUGIN_EXECUTION_DONE, False)
