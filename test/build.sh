#!/bin/sh

set -ex

BSDINSTALLER_DIR="bsd-cloudinit-installer_master"

git clone https://github.com/pellaeon/bsd-cloudinit-installer.git $BSDINSTALLER_DIR

TEST_DIR="$BSDINSTALLER_DIR/test"
TEST_IMG="$TEST_DIR/tester.raw"

export OS_FLAVOR="m1.1G1C"
export OS_NET="110-internal"
export OS_KEYPAIR="fls"

echo $LANG
echo $OS_TENANT_NAME

cd $TEST_DIR

script -a /dev/null ./build.sh
#./build.sh
