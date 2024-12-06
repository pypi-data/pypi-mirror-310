import unittest

from medver_pytest import pth

from ver.core.ver_client import VerClient
from ver.core.ver_server import VerServer
from ver.core.ver_services import VerServices
from ver.helpers.helper import Helper
from ver.mocks.mock_logger import MockLogger


# -------------------
class TestTp001Basic(unittest.TestCase):

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        VerServices.logger = MockLogger()
        VerServices.verbose = True

    # -------------------
    def setUp(self):
        print('')
        VerServices.server = VerServer()

    # -------------------
    def tearDown(self):
        VerServices.server.term()
        VerServices.client.term()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        pth.term()

    # --------------------
    def test_tp001(self):
        pth.proto.protocol('tp-001', 'basic server tests')

        pth.proto.step('start server')
        ok = VerServices.server.init()

        pth.proto.step('verify parameters are set correctly')
        pth.ver.verify_true(ok, reqids='SRS-001')
        pth.ver.verify_equal(VerServices.ip_address, VerServices.server.ols.ip_address, reqids='SRS-001')
        pth.ver.verify_equal(VerServices.ip_port, VerServices.server.ols.ip_port, reqids='SRS-001')
        pth.ver.verify_equal(VerServices.logger, VerServices.server.ols.logger, reqids='SRS-001')
        pth.ver.verify_equal(VerServices.verbose, VerServices.server.ols.verbose, reqids='SRS-001')
        pth.ver.verify_not_none(VerServices.server.ols.callback, reqids='SRS-001')

        pth.proto.step('verify server is running')
        Helper.wait_until_started(5)
        pth.ver.verify(VerServices.server.ols.is_running, reqids='SRS-001')

        pth.proto.step('start client')
        VerServices.client = VerClient()
        VerServices.client.init()
        pth.ver.verify_true(VerServices.client.olc.connected, reqids='SRS-011')

        pth.proto.step('client requests shutdown')
        VerServices.client.shutdown()
        Helper.wait_until_stopped(5)
        pth.ver.verify_false(VerServices.client.olc.connected, reqids='SRS-012')

        pth.proto.step('verify server is not running')
        pth.ver.verify_false(VerServices.server.ols.is_running, reqids='SRS-006')

        VerServices.client.term()
