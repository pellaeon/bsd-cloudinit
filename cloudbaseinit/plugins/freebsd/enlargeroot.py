from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins import base
from cloudbaseinit.openstack.common import log as logging

import subprocess

LOG = logging.getLogger(__name__)

class EnlargeRoot(base.BasePlugin):
    def _call_shell(self, cmd):
        return subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)

    def execute(self, service):
        rootdisk = 'vtbd0'
        self._call_shell('gpart recover ' + rootdisk)
        self._call_shell('sysctl kern.geom.debugflags=16')
        self._call_shell('gpart resize -i 2 ' + rootdisk)
        self._call_shell('growfs -y /dev/' + rootdisk + 'p2')
        return (base.PLUGIN_EXECUTION_DONE, False)
