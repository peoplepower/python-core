import pytest
import unittest
from caredaily import CareDaily

class TestCareDaily(unittest.TestCase):
    def setUp(self):
        pass

    def test_caredaily_init_default(self):
        c = CareDaily(profile=None, raise_errors=False)
        self.assertTrue(hasattr(c, "_config"))
        self.assertIsInstance(c._config, dict)
