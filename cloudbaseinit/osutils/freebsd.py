from cloudbaseinit.osutils import base
import subprocess

class FreeBSDUtils(base.BaseOSUtils):
    def reboot(self):
        if ( os.system('reboot') != 0 ):
            raise Exception('Reboot failed')

    def user_exists(self, username):
        try:
            subprocess.check_output(["id", username])
        except CalledProcessError:
            return False
        return True

    # not completed
    def create_user(self, username, password, invite_group, password_expires=False):
        """
            invite_group must be a list of string.
        """
        home_dir = '/home/' + username
        user_shell = '/bin/tcsh'
        user_comment = 'Created by bsdcloud-init'
        grouplist = ''

        assert isinstance(invite_group, list), "invite_group must be a list."
        assert invite_group, "invite_group cannot be empty."
        for i in invite_group:
            grouplist += i+','
        grouplist = grouplist[:-1]

        pw_cmd = "echo " + password + " | pw useradd -n " + username + " -c '" + user_comment + "' -d '" + user_shell + "' -s /bin/tcsh -h 0 -G " + grouplist
        subprocess.check_call(pw_cmd, shell=True)
        subprocess.check_call("mkdir %s" % (home_dir), shell=True)
        subprocess.check_call("chown -R %s:%s %s" % (username, username, home_dir), shell=True)

    def set_host_name(self, new_host_name):
        try:
            subprocess.check_output(["hostname", new_host_name])
            cmd_newhost = "[ -z `egrep '^hostname' /etc/rc.conf` ] && { echo 'hostname=\"%s\"' >> /etc/rc.conf } || { sed -e 's/^hostname=.*$/hostname=\"%s\"/' -I '' /etc/rc.conf }" % (new_host_name, new_host_name)
            subprocess.check_output(cmd_newhost, shell=True)
            return False
        except CalledProcessError:
            raise Exception(CalledProcessError.output)

    def sanitize_shell_input(self, value):
        pass

    def set_user_password(self, username, password):
        pw_cmd = "echo " + password + " | pw usermod -n " + username + " -h 0"
        subprocess.check_call(pw_cmd, shell=True)

    def add_user_to_local_group(self, username, groupname):
        pass

    def get_user_home(self, username):
        pass

    def get_network_adapters(self):
        """
        This fucntion will return a list of interface.
        """
        if_list = subprocess.check_output(['ifconfig', '-l']).split(' ')
        return if_list

    def set_static_network_config(self, adapter_name, address, netmask,
                                  broadcast, gateway, dnsdomain,
                                  dnsnameservers):
        pass

    def set_config_value(self, name, value, section=None):
        pass

    def get_config_value(self, name, section=None):
        pass

    def wait_for_boot_completion(self):
        pass

    def terminate(self):
        pass

    def get_default_gateway(self):
        """
            We cannot handle mutiple default gateway.
        """
        interface = subprocess.check_output("route get default | grep interface", shell=True).split()[1]
        gateway_ip = subprocess.check_output("route get default | grep gateway", shell=True).split()[1]
        return (interface, gateway_ip)

    def check_static_route_exists(self, destination):
        pass

    def add_static_route(self, destination, mask, next_hop, interface_index,
                         metric):
        pass

    def get_os_version(self):
        pass

    def get_volume_label(self, drive):
        pass
