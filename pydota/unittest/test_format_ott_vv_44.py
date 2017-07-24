#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : test OttVV311Format class
Author : guodong@mgtv.com
Date   : 2016.01.07
"""

import unittest
from pydota.format.format_ott_vv_44 import OttVV44Format


class TestOttVV44Format(unittest.TestCase):
    def setUp(self):
        self.client = OttVV44Format("201512281800")

    def test_getDictByLog(self):
        log_str = ""
        res = self.client.getDictByLog(log_str)
        self.assertEqual(res, [-1, "indexerr"])

        log_str = """2015\t127.0.0.1\t3\t4\t5\t6\t7\tact=play&vid=123&pt=0"""

        res = self.client.getDictByLog(log_str)
        self.assertEqual(res, [-1, "jsonerr"])

        log_str = """2015\t127.0.0.1\t3\t4\t5\t6\t7\t{"act":"play", "pt":0, "vid":123}"""

        res = self.client.getDictByLog(log_str)
        self.assertEqual(res[0], 0)
        self.assertEqual(res[1]['ip'], '127.0.0.1')
        self.assertEqual(res[1]['time'], '2015')
        self.assertEqual(res[1]['vid'], 123)
        self.assertEqual(res[1]['pt'], 0)
        self.assertEqual(res[1]['act'], 'play')

        log_str = """2015\t127.0.0.1\t3\t4\t5\t6\t7\t[{"act":"play", "pt":0, "vid":123}, {"act":"drag", "pt":0, "vid":123}]"""

        res = self.client.getDictByLog(log_str)
        self.assertEqual(res[0], 0)
        self.assertEqual(res[1]['ip'], '127.0.0.1')
        self.assertEqual(res[1]['time'], '2015')
        self.assertEqual(res[1]['vid'], 123)
        self.assertEqual(res[1]['pt'], 0)
        self.assertEqual(res[1]['act'], 'play')

    def test__wash_clientver(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [-1, 'avererr'])

        # log_dict aver不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [-1, 'avererr'])

        # log_dict aver值为空
        log_dict = {"act": "play", "pt": 0, "aver": ""}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [-1, 'avererr'])

        # log_dict aver有值,含需要过滤字符串
        log_dict = {"act": "play", "pt": 0, "aver": "a.b.c.d.e.ShYd19.f"}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [-3, ''])

        # log_dict aver有值,含需要过滤字符串,并在开头
        log_dict = {"act": "play", "pt": 0, "aver": "YYS.a.b.c.d.e.f"}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [-3, ''])

        # log_dict aver有值,不含需要过滤字符串
        log_dict = {"act": "play", "pt": 0, "aver": "Imgo-iPhone-4.4.3"}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [0, 'imgo-iphone-4.4.3'])

if __name__ == '__main__':
    unittest.main()