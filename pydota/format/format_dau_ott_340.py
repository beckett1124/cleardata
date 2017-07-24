#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format dau_ott_340 class
Author : guodong@mgtv.com
Date   : 2016.05.04
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf


class DauOtt340Format(FormatBase):
    """
    dau_ott_340
    """
    def __init__(self, recv_time, topic_name='dau_ott_340'):
        super(DauOtt340Format, self).__init__(recv_time)
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
        _dict = {}
        res_list = log_str.strip().split('\t')
        if len(res_list) < 8:
            return [-1, "indexerr"]
        json_content = res_list[7].strip()
        try:
            _list = json.loads(json_content)
            if isinstance(_list, dict):
                _dict = _list
            elif isinstance(_list, list):
                _dict = _list[0]
            else:
                return [-1, 'jsonerr']
        except ValueError:
            return [-1, 'jsonerr']

        _dict['ip'] = res_list[1]
        _dict['time'] = res_list[0]

        return [0, _dict]

    def _wash_pt(self, log_key, log_dict):
        """
        wash pt, '1'换位'0'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]
        pt = str(log_dict[log_key])
        if pt == '1':
            pt = '0'
        else:
            return [-1, '%serr' % log_key]
        return [0, pt]

    def _wash_clientver(self, log_key, log_dict):
        """
        wash clientver
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys() or log_dict[log_key] == '':
            return [-1, "%serr" % log_key]

        client_ver = str(log_dict[log_key]).lower()

        aver_tmp = client_ver.split('.')
        try:
            if aver_tmp[5] in ["dxjd", "jllt", "fjyd", "shyd19"] or aver_tmp[0] == "yys":
                return [-3, '']
        except IndexError:
            pass

        if client_ver.startswith("4.4."):
            return [0, client_ver]
        else:
            return [-3, "%serr" % log_key]


if __name__ == '__main__':
    start_time = sys.argv[1]
    dau_ott_340_client = DauOtt340Format(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = dau_ott_340_client.processFormat(line)
        # print res[0]
        # print res[1]
