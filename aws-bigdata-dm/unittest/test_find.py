# @Author: jeffrey
# @Date:   2016-05-18T14:27:02+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T14:54:16+08:00
import unittest
import sys
if 'aws-bigdata-matrixing' not in sys.modules and __name__ == '__main__':


class test_find(unittest.TestCase):

    def test_find_string(self):
        print "android".find("android")

if __name__ == '__main__':
    unittest.main()
