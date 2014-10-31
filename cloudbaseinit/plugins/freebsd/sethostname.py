from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins import base
from cloudbaseinit.openstack.common import log as logging

LOG = logging.getLogger(__name__)

class SetHostNamePlugin(base.BasePlugin):
    def execute(self, service, shared_data):
        meta_data = service.get_meta_data('openstack')
        if 'hostname' not in meta_data:
            LOG.debug('Hostname not found in metadata')
            return (base.PLUGIN_EXECUTION_DONE, False)

        osutils = osutils_factory.OSUtilsFactory().get_os_utils()

        new_host_name = meta_data['hostname'].split('.', 1)[0]
        reboot_required = osutils.set_host_name(new_host_name)

        return (base.PLUGIN_EXECUTION_DONE, reboot_required)
