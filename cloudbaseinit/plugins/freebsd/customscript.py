from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins import base
from cloudbaseinit.openstack.common import log as logging

import subprocess
import os

LOG = logging.getLogger(__name__)

class CustomScriptPlugin(base.BasePlugin):
    def _call_shell(self, cmd):
        return subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)

    def execute(self, service):
        user_data = service.get_user_data('openstack')
        script_dir = '/root/scripts'

        if ( !os.path.exists(script_dir) ):
            os.mkdir(script_dir, 0755)
        else
            if( !os.path.isdir(script_dir) ):
                script_dir = '/tmp'

        file_path = '%s/CustomScript.%d' % (script_dir, os.getpid())
        script_file = open(file_path, 'w')
        script_file.write(user_data)
        script_file.close()
        os.chmod(file_path, 0700)
        self._call_shell(file_path)
        os.remove(file_path)

        return (base.PLUGIN_EXECUTION_DONE, False)
