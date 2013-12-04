from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins import base
from cloudbaseinit.openstack.common import log as logging

import subprocess
import os
import tempfile
import uuid

LOG = logging.getLogger(__name__)

class UserDataPlugin(base.BasePlugin):
    def _call_shell(self, cmd):
        return subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)

    def execute(self, service):
        user_data = service.get_user_data('openstack')
        script_dir = '/root/.bsd-cloudinit'

        if ( !os.path.exists(script_dir) ):
            os.mkdir(script_dir, 0755)
        else
            if( !os.path.isdir(script_dir) ):
                LOG.warn('Cannot create dir: ' + script_dir + '.'
                        'Using' + tempfile.gettempdir() + ' instead.')
                script_dir = tempfile.gettempdir()

        file_path = '%s/UserData.%d' % (script_dir, uuid.uuid4())
        script_file = open(file_path, 'w')
        script_file.write(user_data)
        script_file.close()
        #os.chmod(file_path, 0700)
        #self._call_shell(file_path)
        #os.remove(file_path)

        return (base.PLUGIN_EXECUTION_DONE, False)
