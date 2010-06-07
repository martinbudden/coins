"""
coins2utf8 test module.
"""

import unittest
from coins import coins2utf8


class ExampleTestCase(unittest.TestCase):
    """Example test case."""

    def setUp(self):
        """No setUp required."""
        pass

    def tearDown(self):
        """No tearDown required."""
        pass

    def testNormalizeTimeField(self):
        """Test time normalization."""
        result = coins2utf8._normalize_time_field('January 2010 MTH')
        expected = u'2010-01'
        self.assertEqual(result, expected)
        result = coins2utf8._normalize_time_field('2010-02')
        expected = '2010-02'
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
