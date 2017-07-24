#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mpp_vv_mobile_211_20151012_live class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common import check_act_field, check_pt_field


class LiveMppVVMobile211Format(FormatBase):
    """
    mpp_vv_mobile_211_20151012_live
    """
    def __init__(self, recv_time, topic_name='mpp_vv_mobile_211_20151012_live'):
        super(LiveMppVVMobile211Format, self).__init__(recv_time)
        self.name = topic_name
        self.log_all_list = []
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

        if not check_pt_field(json_content, "4"):
            return [-3, _dict]

        if not check_act_field(json_content, "aplay"):
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
            return [-1, 'jsonerr']

        _dict['ip'] = res_list[1]
        _dict['time'] = res_list[0]

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

    def _wash_pt(self, log_key, log_dict):
        """
        wash pt, 必须为4，非4直接丢弃
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys() or log_dict[log_key] == "":
            return [-1, '%serr' % log_dict]

        if log_dict[log_key] != '4':
            return [-3, 'pterr']
        return [0, '4']

if __name__ == '__main__':
    start_time = sys.argv[1]
    live_mobile_211_client = LiveMppVVMobile211Format(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = live_mobile_211_client.processFormat(line)
        # print res[0]
        # print res[1]
