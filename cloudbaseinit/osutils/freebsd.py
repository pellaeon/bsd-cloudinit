from cloudbaseinit.osutils import base

from subprocess import CalledProcessError
import subprocess
import datetime
import os.path

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

    def create_user(self, username, password, invite_group=None, password_expires=False):
        """
        :param invite_group: it must be a list of string.
        """
        home_dir = '/home/' + username
        user_shell = '/bin/tcsh'
        user_comment = 'Created by bsdcloud-init'
        grouplist = ''

        assert not invite_group or isinstance(invite_group, list), "param invite_group must be a list."
        assert invite_group, "invite_group cannot be empty."
        for i in invite_group:
            grouplist += i+','
        grouplist = grouplist[:-1]

        pw_cmd = "echo " + password + " | pw useradd -n " + username + " -c '" + user_comment + "' -d '" + home_dir + "' -s /bin/tcsh -h 0 -G " + grouplist
        subprocess.check_call(pw_cmd, shell=True)
        subprocess.check_call("mkdir -p %s" % (home_dir), shell=True)
        self.chown(username, username, home_dir)

    def set_host_name(self, new_host_name):
        subprocess.check_call(['hostname', new_host_name])
        self._add_rc_conf({'hostname': new_host_name})

    def sanitize_shell_input(self, value):
        pass

    def set_user_password(self, username, password):
        pw_cmd = "echo " + password + " | pw usermod -n " + username + " -h 0"
        subprocess.check_call(pw_cmd, shell=True)

    def add_user_to_local_group(self, username, groupname):
        pw_cmd = 'pw usermod ' + username + ' -G ' + groupname
        subprocess.check_call(pw_cmd, shell=True)

    def get_user_home(self, username):
        home_dir = subprocess.check_output('printf ~' + username, shell=True)
        return home_dir

    def get_network_adapters(self):
        """
        This fucntion will return a list of interface.
        """
        if_list = subprocess.check_output(['ifconfig', '-l']).split(' ')
        # Filter out non-network interfaces
        if_list = filter(lambda x: x.startswith(('pflog', 'lo', 'plip')), if_list)
        return if_list

    def set_static_network_config(self, adapter_name, address, netmask,
                                  broadcast, gateway, dnsdomain,
                                  dnsnameservers):
        """
        :param dnsnameservers: must be a list, it can contain 3 elements at most.
        """
        if_list = self.get_network_adapters()
        assert adapter_name in if_list, 'Network interface: ' + adapter_name + ' not found.'
        assert isinstance(dnsnameservers, list), 'dnsnameservers must be a list.'

        if_cmd = 'ifconfig ' + adapter_name + ' inet ' + address + ' netmask ' + netmask + ' broadcast ' + broadcast
        route_cmd = 'route add default ' + gateway
        resolv_conf = ['domain ' + dnsdomain]
        resolv_conf_file = open('/etc/resolv.conf', 'w')
        for i in dnsnameservers:
            resolv_conf.append('nameserver ' + i)

        subprocess.check_call(if_cmd, shell=True)
        subprocess.check_call(route_cmd, shell=True)
        self._add_comment(resolv_conf_file);
        for line in resolv_conf:
            resolv_conf_file.write(line + '\n')
        self._add_rc_conf({'ifconfig_' + adapter_name: 'inet ' + address + ' netmask ' + netmask + ' broadcast ' + broadcast,
                           'defaultrouter': gateway})

        resolv_conf_file.close()

        # should return reboot_required, which is always false.
        return False

    def set_dhcp_network_config(self, adapter_name):
        if_list = self.get_network_adapters()
        assert adapter_name in if_list, 'Network interface: ' + adapter_name + ' not found.'

        _add_rc_conf({'ifconfig_' + adapter_name: 'DHCP'})
        subprocess.check_call(['dhclient', adapter_name])

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

    def set_timezone(self, timezone, zoneinfo_dir='/usr/share/zoneinfo'):
        """
        :param timezone: The zoneinfo_file path under /usr/share/zoneinfo.
                        e.g: Asia/Taipei
                        Note that this parameter is case-sensitive,
                        because it's the real path under filesystem.
        """
        path = zoneinfo_dir + '/' + timezone
        assert os.path.isfile(path), 'Time zone file not found: ' + path

        subprocess.check_call(['cp', path, '/etc/localtime'])
        subprocess.check_call(['adjkerntz', '-a'])

    def adj_sys_time(self, ntp_server):
        """
        This function will using 'ntpdate' to sync the clock.
        param ntp_server: string of server.
        """
        subprocess.check_call(['ntpdate', '-b', ntp_server])

    def _add_comment(self, file_obj):
        file_obj.write('# Generated by bsdcloud-init ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + '\n')

    def _add_rc_conf(self, options):
        """ For appending new options to /etc/rc.conf
        :param options: an dictionary that contain {'option name': 'value'}
            e.g. {'hostname': 'example',
                   'sshd_enable': 'YES'}
        """
        assert isinstance(options, dict), 'param options must be a dictionary.'
        rc_conf_file = open('/etc/rc.conf', 'a')

        self._add_comment(rc_conf_file)
        for key in options:
            rc_conf_file.write(key + '="' + options[key] + '"\n')

        rc_conf_file.close()

    def chown(self, user, group=None, path=None):
        if path is None:
            return

        subprocess.check_call(
            'chown -R {user}{group} {path}'.format(
                user=user,
                group=':' + group if group else None,
                path=path,
            ),
            shell=True
        )
