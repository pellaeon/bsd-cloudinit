# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Pellaeon Lin <pellaeon@hs.ntnu.edu.tw>
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

from oslo.config import cfg
from cloudbaseinit.openstack.common import log as logging
from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins import base
from cloudbaseinit.plugins import constants

opts = [
    cfg.StrOpt('username', default='freebsd', help='User to be added to the '
               'system or updated if already existing'),
    cfg.ListOpt('groups', default=['wheel'], help='List of local '
                'groups to which the user specified in \'username\' will '
                'be added'),
    cfg.BoolOpt('inject_user_password', default=True, help='Set the password '
                'provided in the configuration. If False or no password is '
                'provided, a random one will be set'),
]

CONF = cfg.CONF
CONF.register_opts(opts)

LOG = logging.getLogger(__name__)


class CreateUserPlugin(base.BasePlugin):
    def _get_password(self, osutils):
        # Generate a temporary random password to be replaced
        # by SetUserPasswordPlugin (starting from Grizzly)
        return osutils.generate_random_password(14)

    def execute(self, service, shared_data):
        user_name = CONF.username
        shared_data[constants.SHARED_DATA_USERNAME] = user_name

        osutils = osutils_factory.get_os_utils()
        password = self._get_password(osutils)

        if osutils.user_exists(user_name):
            LOG.info('Setting password for existing user "%s"' % user_name)
            osutils.set_user_password(user_name, password)
        else:
            LOG.info('Creating user "%s" and setting password' % user_name)
            osutils.create_user(user_name, password, CONF.groups, False)
            shared_data[constants.SHARED_DATA_PASSWORD] = password

        '''for group_name in CONF.groups:
            try:
                osutils.add_user_to_local_group(user_name, group_name)
            except Exception as ex:
                LOG.exception(ex)
                LOG.error('Cannot add user to group "%s"' % group_name)
        '''
        return (base.PLUGIN_EXECUTION_DONE, False)
