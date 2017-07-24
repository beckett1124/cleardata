#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : test PcWeb1110Format class
Author : guodong@mgtv.com
Date   : 2016.01.06
"""

import unittest
from pydota.format.format_pcweb_1110_20151223 import PcWeb1110Format


class TestPcWeb1110Format(unittest.TestCase):
    def setUp(self):
        self.client = PcWeb1110Format("201512281800")

    def test_getDictByLog(self):
        log_str = ""
        res = self.client.getDictByLog(log_str)
        self.assertEqual(res, [-1, "indexerr"])

        log_str = """2015\t127.0.0.1\t3\t4\t5\t6\t7\tact=play&pt=0&vid=123"""

        res = self.client.getDictByLog(log_str)
        self.assertEqual(res[0], 0)
        self.assertEqual(res[1]['ip'], '127.0.0.1')
        self.assertEqual(res[1]['time'], '2015')
        self.assertEqual(res[1]['vid'], '123')
        self.assertEqual(res[1]['pt'], '0')
        self.assertEqual(res[1]['act'], 'play')

if __name__ == '__main__':
    unittest.main()