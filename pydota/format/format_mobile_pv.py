#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mobile_pv class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import ujson
from format_base import FormatBase
from conf_settings import ServerConf


class MobilePvFormat(FormatBase):
    """
    mobile_pv
    """
    def __init__(self, recv_time, topic_name='mobile_pv'):
        super(MobilePvFormat, self).__init__(recv_time)
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
        try:
            _list = ujson.loads(json_content)
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


if __name__ == '__main__':
    start_time = sys.argv[1]
    mobile_pv_client = MobilePvFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mobile_pv_client.processFormat(line)
        # print res[0]
        # print res[1]
