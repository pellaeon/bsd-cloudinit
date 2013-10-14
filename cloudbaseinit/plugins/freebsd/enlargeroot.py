import subprocess

LOG = logging.getLogger(__name__)

class EnlargeRoot(base.BasePlugin):
    def execute(self, service):
        rootdisk = 'vtbd0'
        subprocess.check_call('gpart recover '+rootdisk, shell=True)
        subprocess.check_call('sysctl kern.geom.debugflags=16', shell=True)
        subprocess.check_call('gpart resize -i 2 '+rootdisk, shell=True)
        subprocess.check_call('growfs -y /dev/'+rootdisk+'p2', shell=True)
        return (base.PLUGIN_EXECUTION_DONE, False)
