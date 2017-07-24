#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mpp_vv_mobile_211_20151012 class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common import check_act_field


class MppVVMobile211Format(FormatBase):
    """
    mpp_vv_mobile_new_version
    """
    def __init__(self, recv_time, topic_name='mpp_vv_mobile_211_20151012'):
        super(MppVVMobile211Format, self).__init__(recv_time)
        self.name = topic_name
        self.log_all_list = []
        self.ua_content_dict = {}
        self.des_key_list = ServerConf[self.name]["des_key_list"]
        self.des_dict_list = ServerConf[self.name]["des_dict_list"]
        self.des_dict = ServerConf[self.name]["des_dict"]

    def getDictByLog(self, log_str):
        """
        通过日志获取Dict
        :param log_str:
        :return:
        """
        self.log_all_list = []
        res_list = log_str.strip().split('\t')
        if len(res_list) < 8:
            return [-1, "indexerr"]
        json_content = res_list[7].strip()

        _dict = dict()
        _dict['ip'] = res_list[1]
        _dict['time'] = res_list[0]

        if not check_act_field(json_content, "aplay"):
            if "act=aplay" not in json_content:
                return [-3, _dict]

        try:
            _list = json.loads(json_content)
            if isinstance(_list, dict):
                _dict = _list
                self.log_all_list.append(_dict)
            elif isinstance(_list, list):
                _dict = _list[0]
                self.log_all_list = _list
            else:
                return [-1, 'jsonerr']
        except ValueError:
            res_tmp = self.getDictByUrlNew(json_content, _dict)
            if res_tmp[0] != 0:
                return res_tmp

        _dict['ip'] = res_list[1]
        _dict['time'] = res_list[0]

        ua_content = res_list[4].strip()

        md_log_str = str(_dict.get('mod', "")).strip()

        if 'mod' in _dict and _dict['mod'] != "":
            md_list = str(_dict['mod']).strip().split(' ')
            if len(md_list) > 1:
                md_str = ' '.join(md_list[1:])
            else:
                md_str = str(md_list[0])
            _dict['mod'] = md_str
        else:
            _dict['mod'] = ""

        if 'sver' in _dict and _dict['sver'] != "":
            os_str = str(_dict['sver']).lower()
            if "iphone" in os_str:
                os_str = os_str.replace('iphone', 'iOS')
            elif "ipad" in os_str:
                os_str = os_str.replace('ipad', 'iOS')
            elif "aphone" in os_str:
                os_str = os_str.replace('aphone', 'Android')

            _dict['os'] = self.fix_os(os_str)
        else:
            _dict['os'] = ""

        if str(ua_content) == "":
            return [0, _dict]

        browser_ver_os_list = self.ua_content_dict.get(ua_content)
        if browser_ver_os_list is None:
            res_ua = self.getMobielVVUserAgent(ua_content, _dict)
            if res_ua[1] == "no_cache":
                self.ua_content_dict[ua_content] = []
                return [0, _dict]
            if 'os' in _dict and 'mf' in _dict and 'mod' in _dict:
                self.ua_content_dict[ua_content] = [_dict['os'], _dict['mf'], _dict['mod']]
            else:
                self.ua_content_dict[ua_content] = []
        else:
            if isinstance(browser_ver_os_list, list) and len(browser_ver_os_list) >= 3:
                _dict['os'] = browser_ver_os_list[0]
                _dict['mf'] = browser_ver_os_list[1]
                _dict['mod'] = browser_ver_os_list[2]

        if "iphone" in str(_dict.get('aver', '')).lower():
            _dict['mod'] = md_log_str

        return [0, _dict]

    def _wash_clientver(self, log_key, log_dict):
        """
        wash clientver
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, "%serr" % log_key]
        clientver = str(log_dict[log_key]).lower()
        if "imgotv-aphone" in clientver:
            version = self.getVersionNum(clientver)
            if version[0] != 0:
                return version
            if version[1] < 453:
                return [-1, 'versionNumerr']
        elif "imgotv-iphone" in clientver:
            version = self.getVersionNum(clientver)
            if version[0] != 0:
                return version
            if version[1] < 455:
                return [-1, 'versionNumerr']
        elif "ipad" in clientver:
            version = self.getVersionNum(clientver)
            if version[0] != 0:
                return version
            if version[1] < 423:
                return [-1, 'versionNumerr']

        return [0, clientver]

    def _wash_act(self, log_key, log_dict):
        """
        wash act, 必须为aplay，aplay替换为play
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]

        # 非alay事件直接丢弃,-3
        if log_dict[log_key] != "aplay":
            return [-3, '']
        return [0, "play"]

    def fix_os(self, os_str):
        if str(os_str).endswith(".0"):
            return str(os_str)[0:len(os_str)-2]
        else:
            return str(os_str)


if __name__ == '__main__':
    start_time = sys.argv[1]
    mobile_211_client = MppVVMobile211Format(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mobile_211_client.processFormat(line)
        # print res[0]
        # print res[1]
