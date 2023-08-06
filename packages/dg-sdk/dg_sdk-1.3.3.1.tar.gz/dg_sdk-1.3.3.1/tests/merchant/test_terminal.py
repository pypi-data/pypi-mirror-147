import unittest
from tests.conftest import *


class TestTerminal(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_terminal_add(self):
        result = dg_sdk.Terminal.add()
        assert result["resp_code"] == "20003"

    def test_terminal_cancel(self):
        result = dg_sdk.Terminal.cancel("12123123123123")

        assert result["resp_code"] == "20003"

    def test_terminal_list(self):
        result = dg_sdk.Terminal.query_list()

        assert result["resp_code"] == "20003"
