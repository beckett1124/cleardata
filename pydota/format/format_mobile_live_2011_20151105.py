#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mobile_live_2011_20151105 class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common import check_act_field


class MobileLive2011Format(FormatBase):
    """
    mobile_live_2011_20151105
    """
    def __init__(self, recv_time, topic_name='mobile_live_2011_20151105'):
        super(MobileLive2011Format, self).__init__(recv_time)
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
        wash act
        :param log_key:
        :param log_dict:
        :return:
        """
        if log_key not in log_dict.keys():
            # 有些版本act在里层json数组里
            _act = ''
        else:
            _act = log_dict[log_key]

        if "aver" not in log_dict.keys():
            return [-1, 'avererr']
        _ver = log_dict["aver"]
        ver = _ver.lower()
        pro_ver = ''
        if 'iphone' in ver:
            res_tmp = self.getVersionNum(ver)
            if res_tmp[0] != 0:
                return res_tmp
            if res_tmp[1] < 454:
                pro_ver = 'iphone_low_454'
            else:
                pro_ver = 'iphone454'
        elif 'aphone' in ver:
            res_tmp = self.getVersionNum(ver)
            if res_tmp[0] != 0:
                return res_tmp
            if res_tmp[1] >= 452:
                pro_ver = 'aphone_than_452'
            else:
                pro_ver = 'aphone_low_452'
        elif ver == '4.5.2':
            pro_ver = 'aphone452'
        else:
            pro_ver = "aphone_low_452"

        if pro_ver in ['aphone452', 'iphone454', 'aphone_than_452']:
            if _act == 'aplay':
                return [0, 'play']
            else:
                return [-3, 'not aplay']
        elif pro_ver in ['iphone_low_454', 'aphone_low_452']:
            for i in range(len(self.log_all_list)):
                if self.log_all_list[i].get('act', '') == 'play':
                    return [0, 'play']
            return [-3, 'not play']
        else:
            if _act == 'aplay':
                return [0, 'play']
        return [-1, '%serr' % log_key]


if __name__ == '__main__':
    start_time = sys.argv[1]
    mobile_live_2011_client = MobileLive2011Format(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mobile_live_2011_client.processFormat(line)
        # print res[0]
        # print res[1]
