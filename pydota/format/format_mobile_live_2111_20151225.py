#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mobile_live_2111_20151225 class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common import check_act_field


class MobileLive2111Format(FormatBase):
    """
    mobile_live_2111_20151225
    """
    def __init__(self, recv_time, topic_name='mobile_live_2111_20151225'):
        super(MobileLive2111Format, self).__init__(recv_time)
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

        if not check_act_field(json_content, "play", "aplay"):
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

    def _wash_clienttp(self, log_key, log_dict):
        """
        wash clienttp,
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys() or log_dict[log_key] == "":
            return [-1, '%serr' % log_key]
        value = str(log_dict[log_key]).lower()
        if 'apad' in value:
            tp = 'apad'
        elif 'ipad' in value:
            tp = 'ipad'
        elif 'iphone' in value:
            tp = 'iphone'
        else:
            tp = 'android'
        return [0, tp]

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
        wash pt, 非ipad必须为4，ipad为1,置为4
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]

        if "aver" not in log_dict.keys():
            return [-1, 'avererr']

        if "ipad" in str(log_dict["aver"].lower()):
            if str(log_dict[log_key]) == "1" or str(log_dict[log_key]) == "4":
                return [0, 4]
            else:
                return [-1, 'pterr']
        else:
            if str(log_dict[log_key]) == "4":
                return [0, 4]
            else:
                return [-1, 'pterr']

    def _wash_sourceid(self, log_key, log_dict):
        """
        wash sourceid, 非ipad必须取lid，ipad取sourceid
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        sourceid = ""
        if log_key in log_dict.keys():
            sourceid = str(log_dict[log_key])
        elif "sourceid" in log_dict.keys():
            sourceid = str(log_dict["sourceid"])

        if sourceid == "":
            return [-1, 'sourceiderr']

        return [0, sourceid]


if __name__ == '__main__':
    start_time = sys.argv[1]
    mobile_live_2111_client = MobileLive2111Format(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mobile_live_2111_client.processFormat(line)
        # print res[0]
        # print res[1]
