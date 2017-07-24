#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T11:01:54+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T15:00:16+08:00


import unittest
import sys
if 'aws-bigdata-matrixing' not in sys.modules and __name__ == '__main__':
from rule.rule import rule
from rule.comm_rule import com_date_year


class TestInstance(unittest.TestCase):

    def test_instance(self):
        year=com_date_year()
        print isinstance(year,rule)

if __name__ == '__main__':
    unittest.main()
