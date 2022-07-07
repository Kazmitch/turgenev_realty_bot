import unittest
from realty_bot.realty_bot.utils import correct_phone


class TestUtils(unittest.TestCase):
    def test_phone(self):
        self.assertEqual(correct_phone('+7 915 333 22-11'), '79153332211')
        self.assertEqual(correct_phone('+7(915)333 22-11'), '79153332211')
        self.assertEqual(correct_phone('(915)333 22-11'), '79153332211')
        self.assertEqual(correct_phone('8 915 333 22-11'), '79153332211')
        self.assertEqual(correct_phone('9153332211'), '79153332211')
        self.assertEqual(correct_phone('89153332211'), '79153332211')

        self.assertEqual(correct_phone('8915333221'), None)
        self.assertEqual(correct_phone('+7915333221'), None)
        self.assertEqual(correct_phone('+791533322111'), None)
