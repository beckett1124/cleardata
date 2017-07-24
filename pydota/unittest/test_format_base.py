#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : test format base class
Author : guodong@mgtv.com
Date   : 2015.12.02
"""

import unittest
from pydota.format.format_base import FormatBase


class TestFormatBase(unittest.TestCase):

    def setUp(self):
        self.client = FormatBase("201512021000")
        self.client.des_key_list = ['act', 'pt', 'cookie', 'xxx', 'abc']
        self.client.des_dict_list = ['cookie', 'act', 'pt', 'xxx', 'abc']
        self.client.des_dict = {'act': ['act', 0], 'pt': ['pt', 1], 'cookie': ['did', 4], 'xxx': ['xxx', 2, 'test'], 'abc': ['abc', 3, 'xx|aaa']}

    def test_getVersionNum(self):
        # 正常版本号,'_'切割
        version = self.client.getVersionNum("imgotv_iphone_4.5.5")
        self.assertEqual(version, [0, 455])

        # 正常版本号,'-'切割
        version = self.client.getVersionNum("imgotv-aphone-4.2.2")
        self.assertEqual(version, [0, 422])

        # 非正常版本
        version = self.client.getVersionNum("aphon-4.3.2")
        self.assertEqual(version, [-1, 'versionNumerr'])

        # 非正常版本
        version = self.client.getVersionNum("imgotv-aphon-43a")
        self.assertEqual(version, [-1, 'versionNumerr'])

    def test_formatLocation(self):

        location = self.client.formatLocation("127.0.0.1")
        self.assertEqual(location, [2130706433, '\xe6\x9c\xac\xe6\x9c\xba\xe5\x9c\xb0\xe5\x9d\x80', '\xe6\x9c\xac\xe6\x9c\xba\xe5\x9c\xb0\xe5\x9d\x80', '*', '*'])

        # 多个ip
        location = self.client.formatLocation("127.0.0.1,10.100.1.141")
        self.assertEqual(location, None)

    def test_getDictByUrl(self):
        # content = "/s.gif?uuid=B49EDB34-A43A-AC86-B0EA-A1D34B7FD9B2&guid=&ref=&os=20&ua=20&" \
        #           "url=null&bid=1&vid=1851597&vts=6361&cid=1&tid=1&plid=159187&" \
        #           "cookie=55D5AE37-E6C5-E87F-8DC9-6F4406D107E4&uid=&did=&ct=0&et=&td=&idx=&" \
        #           "adid=&adtpid=&adtms=&cdnip=pcvideomzc.titan.imgo.tv&pt=flash&tp=1&ln=&cf=1&" \
        #           "isdrm=0&purl=http%3A%2F%2Fpcvideomzc.titan.imgo.tv%2Fmp4%2F2015%2Fzongyi%2Fqyjs" \
        #           "z_37206%2F8E46D72B76A2969C3114739A33A0A5FC_20151121_1_1_717.mp4%2Fplaylist.m3u8%3F" \
        #           "uuid%3D9adb8e249381423abff2ee0cd5e31432%26t%3D565256ea%26win%3D3600%26pno%3D1000%26sr" \
        #           "gid%3D25007%26urgid%3D1867%26srgids%3D25007%26nid%3D25007%26payload%3Dusertoken%" \
        #           "253duuid%253d9adb8e249381423abff2ee0cd5e31432%255eruip%253d1899629759%255ehit%253d0%" \
        #           "26rdur%3D21600%26arange%3D0%26limitrate%3D1050%26fid%3D8E46D72B76A2969C3114739A33A0A5FC%" \
        #           "26sign%3Dde5a04d3d3c2e46018d4ab069d811076%26ver%3D0x03%26r%3D3936676320999&" \
        #           "definition=2&pver=WIN%2011,1,102,63&act=play"
        content = "/s.gif?guid=&ref=&os=20&act=play"
        result = {"guid": "", "ref": "", "os": '20', "act": "play"}
        _dict = {}
        _res = self.client.getDictByUrl(content, _dict)
        self.assertEqual(_res, [0, ''])
        self.assertEqual(_dict, result)

        content = "/s.gif?guid=&ref&os=20&act=play"
        result = {"guid": "", "os": '20', "act": "play"}
        _dict = {}
        _res = self.client.getDictByUrl(content, _dict)
        self.assertEqual(_res, [0, ''])
        self.assertEqual(_dict, result)

        content = ""
        _dict = {}
        _res = self.client.getDictByUrl(content, _dict)
        self.assertEqual(_res, [-1, 'indexerr'])

    def test_getDictByUrlNew(self):
        content = "guid=&ref=&os=20&act=play"
        result = {"guid": "", "ref": "", "os": '20', "act": "play"}
        _dict = {}
        _res = self.client.getDictByUrlNew(content, _dict)
        self.assertEqual(_res, [0, ''])
        self.assertEqual(_dict, result)

        content = "guid=&ref&os=20&act=play"
        result = {"guid": "", "os": '20', "act": "play"}
        _dict = {}
        _res = self.client.getDictByUrlNew(content, _dict)
        self.assertEqual(_res, [0, ''])
        self.assertEqual(_dict, result)

        content = ""
        _dict = {}
        _res = self.client.getDictByUrlNew(content, _dict)
        self.assertEqual(_res, [-1, 'indexerr'])

    def test__wash_tid(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_tid("tid", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict tid不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_tid("tid", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict tid值为空
        log_dict = {"act": "play", "pt": 0, "tid": ""}
        _res = self.client._wash_tid("tid", log_dict)
        self.assertEqual(_res, [0, ''])

        # log_dict tid有值,不含逗号
        log_dict = {"act": "play", "pt": 0, "tid": "1234"}
        _res = self.client._wash_tid("tid", log_dict)
        self.assertEqual(_res, [0, '1234'])

        # log_dict tid有值,含逗号
        log_dict = {"act": "play", "pt": 0, "tid": "1234,2234"}
        _res = self.client._wash_tid("tid", log_dict)
        self.assertEqual(_res, [0, '1234_2234'])

    def test__wash_ref(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_ref("ref", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict ref不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_ref("ref", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict ref值为空
        log_dict = {"act": "play", "pt": 0, "ref": ""}
        _res = self.client._wash_ref("ref", log_dict)
        self.assertEqual(_res, [0, ''])

        # log_dict ref有值,不含逗号,未编码
        log_dict = {"act": "play", "pt": 0, "ref": "http://www.hunantv.com?"}
        _res = self.client._wash_ref("ref", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?'])

        # log_dict ref有值,含逗号,未编码
        log_dict = {"act": "play", "pt": 0, "ref": "http://www.hunantv.com?,xxx"}
        _res = self.client._wash_ref("ref", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?xxx'])

        # log_dict ref有值,不含逗号,编码
        log_dict = {"act": "play", "pt": 0, "ref": "http%3a%2f%2fwww.hunantv.com%3f"}
        _res = self.client._wash_ref("ref", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?'])

        # log_dict ref有值,含逗号,编码
        log_dict = {"act": "play", "pt": 0, "ref": "http%3a%2f%2fwww.hunantv.com%3f%2c%e8%8a%92%e6%9e%9c"}
        _res = self.client._wash_ref("ref", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?芒果'])

    def test__wash_cookie(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_cookie("cookie", log_dict)
        self.assertEqual(_res, [-1, 'cookieerr'])

        # log_dict cookie不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_cookie("cookie", log_dict)
        self.assertEqual(_res, [-1, 'cookieerr'])

        # log_dict cookie值为空
        log_dict = {"act": "play", "pt": 0, "cookie": ""}
        _res = self.client._wash_cookie("cookie", log_dict)
        self.assertEqual(_res, [-1, 'cookieerr'])

        # log_dict cookie有值,不含大写
        log_dict = {"act": "play", "pt": 0, "cookie": "a12b12c12"}
        _res = self.client._wash_cookie("cookie", log_dict)
        self.assertEqual(_res, [0, 'a12b12c12'])

        # log_dict cookie有值,含大写
        log_dict = {"act": "play", "pt": 0, "cookie": "A12B12c12"}
        _res = self.client._wash_cookie("cookie", log_dict)
        self.assertEqual(_res, [0, 'a12b12c12'])

    def test__wash_date(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_date("time", log_dict)
        self.assertEqual(_res, [-1, 'timeerr'])

        # log_dict time不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_date("time", log_dict)
        self.assertEqual(_res, [-1, 'timeerr'])

        # log_dict time值为空
        log_dict = {"act": "play", "pt": 0, "time": ""}
        _res = self.client._wash_date("time", log_dict)
        self.assertEqual(_res, [0, ''])

        # log_dict time有值
        log_dict = {"act": "play", "pt": 0, "time": "20151226101002"}
        _res = self.client._wash_date("time", log_dict)
        self.assertEqual(_res, [0, '20151226'])

    def test__wash_time(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_time("time", log_dict)
        self.assertEqual(_res, [-1, 'timeerr'])

        # log_dict time不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_time("time", log_dict)
        self.assertEqual(_res, [-1, 'timeerr'])

        # log_dict time值为空
        log_dict = {"act": "play", "pt": 0, "time": ""}
        _res = self.client._wash_time("time", log_dict)
        self.assertEqual(_res, [0, ''])

        # log_dict time有值,不含大写
        log_dict = {"act": "play", "pt": 0, "time": "20151226101002"}
        _res = self.client._wash_time("time", log_dict)
        self.assertEqual(_res, [0, '101002'])

    def test__wash_province(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_province("ip", log_dict)
        self.assertEqual(_res, [-1, 'iperr'])

        # log_dict ip不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_province("ip", log_dict)
        self.assertEqual(_res, [-1, 'iperr'])

        # log_dict ip值为空
        log_dict = {"act": "play", "pt": 0, "ip": ""}
        _res = self.client._wash_province("ip", log_dict)
        self.assertEqual(_res, [-1, 'locationerr'])

        # log_dict ip有值,异常ip
        log_dict = {"act": "play", "pt": 0, "ip": "a12b12c12"}
        _res = self.client._wash_province("ip", log_dict)
        self.assertEqual(_res, [-1, 'locationerr'])

        # log_dict ip有值,正常ip
        log_dict = {"act": "play", "pt": 0, "ip": "111.122.158.161"}
        _res = self.client._wash_province("ip", log_dict)
        self.assertEqual(_res, [0, '贵州'])

    def test__wash_city(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_city("ip", log_dict)
        self.assertEqual(_res, [-1, 'iperr'])

        # log_dict cookie不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_city("ip", log_dict)
        self.assertEqual(_res, [-1, 'iperr'])

        # log_dict cookie值为空
        log_dict = {"act": "play", "pt": 0, "ip": ""}
        _res = self.client._wash_city("ip", log_dict)
        self.assertEqual(_res, [-1, 'locationerr'])

        # log_dict cookie有值,不含大写
        log_dict = {"act": "play", "pt": 0, "ip": "a12b12c12"}
        _res = self.client._wash_city("ip", log_dict)
        self.assertEqual(_res, [-1, 'locationerr'])

        # log_dict cookie有值,含大写
        log_dict = {"act": "play", "pt": 0, "ip": "111.122.158.161"}
        _res = self.client._wash_city("ip", log_dict)
        self.assertEqual(_res, [0, '都匀'])

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
        self.assertEqual(_res, [-1, 'avererr'])

        # log_dict aver有值,不含iphone等
        log_dict = {"act": "play", "pt": 0, "aver": "4.5.2"}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [-1, 'clienttperr'])

        # log_dict aver有值
        log_dict = {"act": "play", "pt": 0, "aver": "imgo-iphone-4.4.3"}
        _res = self.client._wash_clienttp("aver", log_dict)
        self.assertEqual(_res, [0, 'iphone'])

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

        # log_dict aver有值,全小写
        log_dict = {"act": "play", "pt": 0, "aver": "imgo-iphone-4.4.3"}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [0, 'imgo-iphone-4.4.3'])

        # log_dict aver有值,含大写
        log_dict = {"act": "play", "pt": 0, "aver": "Imgo-iPhone-4.4.3"}
        _res = self.client._wash_clientver("aver", log_dict)
        self.assertEqual(_res, [0, 'imgo-iphone-4.4.3'])

    def test__wash_ln(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_ln("ln", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict ln不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_ln("ln", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict ln值为空
        log_dict = {"act": "play", "pt": 0, "ln": ""}
        _res = self.client._wash_ln("ln", log_dict)
        self.assertEqual(_res, [0, ''])

        # log_dict ln有值,不含逗号,未编码
        log_dict = {"act": "play", "pt": 0, "ln": "hunantv"}
        _res = self.client._wash_ln("ln", log_dict)
        self.assertEqual(_res, [0, 'hunantv'])

        # log_dict ln有值,含逗号,编码
        log_dict = {"act": "play", "pt": 0, "ln": "http%3a%2f%2fwww.hunantv.com%3f%2c%e8%8a%92%e6%9e%9c"}
        _res = self.client._wash_ln("ln", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?,芒果'])

    def test__wash_url(self):
        # log_dict 为空
        log_dict = {}
        _res = self.client._wash_url("url", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict url不存在
        log_dict = {"act": "play", "pt": 0}
        _res = self.client._wash_url("url", log_dict)
        self.assertEqual(_res, [0, '-'])

        # log_dict url值为空
        log_dict = {"act": "play", "pt": 0, "url": ""}
        _res = self.client._wash_url("url", log_dict)
        self.assertEqual(_res, [0, ''])

        # log_dict url有值,不含逗号,未编码
        log_dict = {"act": "play", "pt": 0, "url": "http://www.hunantv.com?"}
        _res = self.client._wash_url("url", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?'])

        # log_dict url有值,含逗号,未编码
        log_dict = {"act": "play", "pt": 0, "url": "http://www.hunantv.com?,xxx"}
        _res = self.client._wash_url("url", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?xxx'])

        # log_dict url有值,不含逗号,编码
        log_dict = {"act": "play", "pt": 0, "url": "http%3a%2f%2fwww.hunantv.com%3f"}
        _res = self.client._wash_url("url", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?'])

        # log_dict url有值,含逗号,编码
        log_dict = {"act": "play", "pt": 0, "url": "http%3a%2f%2fwww.hunantv.com%3f%2c%e8%8a%92%e6%9e%9c"}
        _res = self.client._wash_url("url", log_dict)
        self.assertEqual(_res, [0, 'http://www.hunantv.com?芒果'])

    def test_runMyWash(self):
        # des_key存在对应的wash函数
        log_dict = {"act": "play", "pt": 0, "did": "a12b12C12"}
        _res = self.client.runMyWash("cookie", "did", log_dict)
        self.assertEqual(_res, [0, 'a12b12c12'])

        # des_key对应的wash函数不存在
        _res = self.client.runMyWash("bad_key", "did", log_dict)
        self.assertEqual(_res, [-2, 'no function[_wash_bad_key] for did '])

    def test_gen_des_dict(self):
        log_dict = {"act": "play", "pt": 0, "did": "a12b12C12", 'abc': "aaa", 'ffff': 'xx'}
        _res = self.client.gen_des_dict(log_dict)
        expect_res = {'abc': 'aaa', 'act': 'play', "cookie": 'a12b12c12', 'pt': '0', 'xxx': "test"}
        flag = 0
        self.assertEqual(_res[0], 0)
        for key in self.client.des_dict_list:
            if key not in _res[1].keys():
                flag = 1
                break
            if _res[1][key] != expect_res[key]:
                flag = 1
                break
        self.assertEqual(flag, 0)

    def test_gen_des_line(self):
        log_dict = {"act": "play", "pt": 0, "did": "a12b12C12", 'abc': "aaa", 'ffff': 'xx'}
        _res_tmp = self.client.gen_des_dict(log_dict)

        _res = self.client.gen_des_line(_res_tmp[1])
        self.assertEqual(_res, [0, "play,0,a12b12c12,test,aaa"])


if __name__ == '__main__':
    unittest.main()