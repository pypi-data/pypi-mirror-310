import unittest
from id32 import id32

class TestID32(unittest.TestCase):
    def test_length(self):
        self.assertEqual(len(id32()), 32)

    def test_characters(self):
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz234567'
        identifier = id32()
        for char in identifier:
            self.assertIn(char, allowed_chars)

if __name__ == '__main__':
    unittest.main()