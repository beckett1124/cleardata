#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format ott_vv_311 class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf


class OttVV311Format(FormatBase):
    """
    ott_vv_311
    """
    def __init__(self, recv_time, topic_name='ott_vv_311_20151012'):
        super(OttVV311Format, self).__init__(recv_time)
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
            res_tmp = self.getDictByUrlNew(json_content, _dict)
            if res_tmp[0] != 0:
                return res_tmp
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
        if log_key not in log_dict.keys() or log_dict[log_key] == '':
            return [-1, "%serr" % log_key]

        client_ver = str(log_dict[log_key]).lower()

        aver_tmp = client_ver.split('.')
        try:
            if aver_tmp[5] in ["dxjd", "jllt", "fjyd", "shyd19"] or aver_tmp[0] == "yys":
                return [-3, '']
        except IndexError:
            return [0, client_ver]

        return [0, client_ver]


if __name__ == '__main__':
    start_time = sys.argv[1]
    ott_vv_311_client = OttVV311Format(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = ott_vv_311_client.processFormat(line)
        # print res[0]
        # print res[1]
