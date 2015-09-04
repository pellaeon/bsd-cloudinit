import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from cloudbaseinit.osutils.freebsd import FreeBSDUtils
from pytest import raises


class TestFreeBSDUtils():
    def setup_method(self, method):
        self.bsd = FreeBSDUtils()

    def teardown_method(self, method):
        del self.bsd

    @mock.patch('cloudbaseinit.osutils.freebsd.os.system', return_value=1)
    def test_reboot(self, system):
        with raises(OSError):
            self.bsd.reboot()

    def test_user_exists(self):
        assert not self.bsd.user_exists('stranger')
        assert self.bsd.user_exists('root')
