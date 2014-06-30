## FreeBSD on OpenStack
There has not been a complete solution to run FreeBSD instances on OpenStack, until now.

With bsd-cloudinit and bsd-cloudinit-installer, you could build a FreeBSD VM image that takes advantage of the cloud environment.

## Components
The entire project to run FreeBSD on OpenStack is called Feng Li Su (鳳梨酥), a kind of cuboid-shaped sweet Taiwanese pastry with soft crust and pineapple fillings.

bsd-cloudinit-installer installs bsd-cloudinit, and make `/etc/rc.local` invoke bsd-cloudinit at first boot.
### [bsd-cloudinit](https://github.com/pellaeon/bsd-cloudinit)
bsd-cloudinit is a Python script based on [cloudbase-init](https://github.com/cloudbase/cloudbase-init/) that do various tasks to prepare the FreeBSD instance for cloud environment.

Features:
* Set hostname according to OpenStack's instance name
* Automatic SSH host key generation
* Enlarge root partition to what the flavor provides
* SSH public key injection
* View instances' console message in OpenStack console log
* Self removal after first boot

### [bsd-cloudinit-installer](https://github.com/pellaeon/bsd-cloudinit-installer)
A shell script to transform VM into OpenStack VM Template and installs bsd-cloudinit

Features:
* Clean SSH host key
* Downloads and install bsd-cloudinit
* Add bsd-cloudinit to `/etc/rc.local`

## Built image
We have [experimental built images](http://images.openstack.nctu.edu.tw/bsd-cloudinit/) available for download.

You can use the following command to upload the image to Glance

    glance image-create --name "FreeBSD 9.2" --disk-format qcow2 \
     --container-format bare < freebsd-9.2-fls-cloudimage-v3.img

bsd-cloudinit will inject your SSH public key into the instance, just log in with username `freebsd`.

The root password is `fenglisu`.

## Build a FreeBSD VM image for OpenStack
If you would like to build your own image, follow the guides below.

bsd-cloudinit-installer is the VM image maker, it transforms a VM into a OpenStack VM image.

### Install FreeBSD via virt-manager
First you'll have to install a normal FreeBSD 9.2 (only 9.2 is tested) VM via virt-manager or similiar tools.

The virtual disk size should be as small as possible, so it'll be quicker to deploy and upload. FreeBSD 9.2 requires root partition to be at least 1GB, so you should create a virtual disk slightly larger than 1GB. (We use 1.1GB in our released experimental images.)

The **root partition must be the last partition on the disk**, so that bsd-cloudinit could grow the partition on first boot.

There should be no need for SWAP. (there is no SWAP in the official Ubuntu cloud images either) But if you want SWAP, always make sure `/` is on the last partition.

After installation completes, do the following actions **as root** to prepare the VM for transformation.

### VIRTIO
Since 9.2 FreeBSD has VIRTIO drivers built into GENERIC kernel, so just change `ada` to `vtbd` in `/etc/fstab`. It'll pick it up on boot.

### Output to OpenStack console log
    echo 'console="comsonsole,vidconsole"' >> /boot/loader.conf
### Bootloader menu delay
    echo 'autoboot_delay="1"' >> /boot/loader.conf
### Download and execute bsd-cloudinit-installer
    fetch https://raw.github.com/pellaeon/bsd-cloudinit-installer/master/installer.sh
    chmod +x installer.sh
    ./installer.sh

After this step, the VM is no longer a normal VM and not suitable for use with virt-manager.

Follow instruction of the installer to clean command history.

Shutdown

    shutdown -p now

After shutting down, the VM's virtual disk is ready to be deployed in OpenStack, just upload it to Glance

    glance image-create --name "FreeBSD 9.2" --disk-format qcow2 \
     --container-format bare < freebsd-9.2-fls-cloudimage-v3.img

Then the image is ready to be deployed! Launch an instance to test it!

## Planned Features
* insert customization script
* `ntpdate` on first boot
* commandline options for the installer
* install `sudo` and remove hardcoded `root` password

## Changelog
* 1312041: Fix `/home/freebsd` wrong permission.

## Authors and Contributors
bsd-cloudinit is built by @pellaeon, @apua, @iblis17 from Information Technology Service Center
 of National Chiao Tung University in Taiwan.

* @pellaeon is the maintainer and takes care of the documentation, planning, coordinating, communications with users.
* @iblis17 takes care of the shell script parts.
* @apua takes care of the Python bits.

This project is based on [cloudbase-init](https://github.com/cloudbase/cloudbase-init), we share most of non-OS-specific code.
## Donation
If you like our project, please consider sending Bitcoin to `17sei77Rt29wQ7cx4hqznQ2esMA49Fj9KQ`
