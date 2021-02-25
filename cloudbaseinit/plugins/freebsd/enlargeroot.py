from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins.common import base
from cloudbaseinit.openstack.common import log as logging

import re
import subprocess

LOG = logging.getLogger(__name__)

class EnlargeRoot(base.BasePlugin):
    def _call_shell(self, cmd):
        return subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)

    def _call_shell_output(self, cmd):
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

    def execute(self, service, shared_data):
        rootdisk = 'vtbd0'

        # We might have swap before the root partition
        gpart_output = self._call_shell_output('gpart show -p ' + rootdisk)
        regex = rootdisk + r'p(?P<part>[0-9]+)\s+freebsd-(?P<fs>(u|z)fs)'
        match = re.search(regex, gpart_output)
        partition = match.group('part')
        filesystem = match.group('fs')

        self._call_shell('gpart recover ' + rootdisk)
        current_debugflags = self._call_shell_output('sysctl -n kern.geom.debugflags')
        self._call_shell('sysctl kern.geom.debugflags=16')
        self._call_shell('gpart resize -i ' + partition + ' ' + rootdisk)

        if filesystem == 'ufs':
            self._call_shell('growfs -y /dev/' + rootdisk + 'p' + partition)
        elif filesystem == 'zfs':
            self._call_shell('zpool set autoexpand=on zroot')
            self._call_shell('zpool online -e zroot ' + rootdisk + 'p' + partition)
        self._call_shell('sysctl kern.geom.debugflags=' + current_debugflags)
        return (base.PLUGIN_EXECUTION_DONE, False)
