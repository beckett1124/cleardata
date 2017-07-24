#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : test RtLivePcWebFormat class
Author : guodong@mgtv.com
Date   : 2016.01.06
"""

import unittest
from pydota.format.format_rt_live_pcweb import RtLivePcWebFormat


class TestRtLivePcWebFormat(unittest.TestCase):
    def setUp(self):
        self.client = RtLivePcWebFormat("201512281800")

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

    def test__wash_clienttp(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [-1, 'avererr'])

        # log_dict aver不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [-1, 'avererr'])

        # log_dict aver值为空
        log_dict = {"act": "play", "pt": 0, "aver": ""}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [-1, ''])

        # log_dict aver为1
        log_dict = {"act": "play", "pt": 0, "aver": "1"}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [0, 'pcclient'])

        # log_dict aver为0
        log_dict = {"act": "play", "pt": 0, "aver": "0"}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [0, 'pcweb'])

        # log_dict aver为2
        log_dict = {"act": "play", "pt": 0, "aver": "2"}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [-1, ''])

if __name__ == '__main__':
    unittest.main()