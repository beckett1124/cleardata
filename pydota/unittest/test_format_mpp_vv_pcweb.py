#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : test PcWeb1110Format class
Author : guodong@mgtv.com
Date   : 2016.01.06
"""

import unittest
from pydota.format.format_mpp_vv_pcweb import MppVVPcWebFormat


class TestMppVVPcWebFormat(unittest.TestCase):
    def setUp(self):
        self.client = MppVVPcWebFormat("201512281800")

    def test_getDictByLog(self):
        log_str = ""
        res = self.client.getDictByLog(log_str)
        self.assertEqual(res, [-1, "indexerr"])

        log_str = """100.91.75.201, 120.210.221.147 - - [21/Jan/2016:00:02:46 +0800] "GET /pcc/pcc.gif?act=play&os=WindowsNT5.1\""""

        res = self.client.getDictByLog(log_str)
        print res
        # self.assertEqual(res[0], 0)
        # self.assertEqual(res[1]['ip'], '127.0.0.1')
        # self.assertEqual(res[1]['time'], '2015')
        # self.assertEqual(res[1]['vid'], '123')
        # self.assertEqual(res[1]['pt'], '0')
        # self.assertEqual(res[1]['act'], 'play')

if __name__ == '__main__':
    unittest.main()