import unittest
from datetime import datetime, timedelta
from sarunas_k_mod1_atsiskaitymas.web_read import crowl, check_time

class TestWeb_read(unittest.TestCase):

    def test_crowl(self):
        self.assertRaises(TypeError,crowl("1",".txt", 20))
        self.assertRaises(TypeError, crowl(1, 2, 20))
        self.assertRaises(TypeError, crowl(1, ".txt", '20'))

