#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format ott_pv class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf


class OttPvFormat(FormatBase):
    """
    ott_vv_41
    """
    def __init__(self, recv_time, topic_name='ott_pv'):
        super(OttPvFormat, self).__init__(recv_time)
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

    def _wash_cookie(self, log_key, log_dict):
        """
        wash cookie, 转小写
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if "aver" not in log_dict.keys() or log_dict["aver"] == "":
            return [-1, 'avererr']
        apk_ver_list = str(log_dict["aver"]).lower().split(".")

        if len(apk_ver_list) >= 6 and apk_ver_list[5] == "sx":
            if "did" not in log_dict.keys() or log_dict["did"] == "":
                return [-1, 'diderr']
            cookie = str(log_dict["did"]).lower()
        else:
            if log_key not in log_dict.keys() or log_dict[log_key] == "":
                return [-1, '%serr' % log_key]
            cookie = str(log_dict[log_key])
        return [0, cookie]


if __name__ == '__main__':
    start_time = sys.argv[1]
    ott_pv_client = OttPvFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = ott_pv_client.processFormat(line)
        # print res[0]
        # print res[1]
