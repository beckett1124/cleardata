#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mglive_base class
Author : guodong@mgtv.com
Date   : 2016.04.26
"""

import sys
import fileinput
import time
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common import is_internal_ip


class MgLiveBaseFormat(FormatBase):
    """
    mglive_base
    """
    def __init__(self, recv_time, topic_name='mglive_base'):
        super(MgLiveBaseFormat, self).__init__(recv_time)
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
        record_tmp = log_str.strip().split('- -')
        if len(record_tmp) < 2:
            return [-1, "indexerr"]

        # 获取ip
        ip_list = record_tmp[0].strip().split(',')
        ip_str = ""
        if len(ip_list) > 1:
            for i in range(len(ip_list)):
                ip_tmp = ip_list[i].strip()
                if is_internal_ip(ip_tmp):
                    continue
                else:
                    ip_str = ip_tmp
                    break
            if ip_str == "":
                ip_str = ip_list[-1].strip()
        else:
            ip_str = ip_list[0].strip()

        # 获取上报日志
        res_list = record_tmp[1].strip().split(' ')

        if len(res_list) < 4:
            return [-1, "indexerr"]
        url_content = res_list[3]
        res_tmp = self.getDictByUrl(url_content, _dict)

        if res_tmp[0] != 0:
            return res_tmp
        _dict['ip'] = ip_str
        time_tmp = res_list[0]
        try:
            time_data = time.strptime(time_tmp, '[%d/%b/%Y:%H:%M:%S')
            _dict['time'] = time.strftime('%Y%m%d%H%M%S', time_data)
        except ValueError:
            return [-1, "timeerr"]

        return [0, _dict]

    def _wash_auid(self, log_key, log_dict):
        """
        wash auid, 值为空时，置为none
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]

        if log_dict[log_key] == "":
            auid = "none"
        else:
            auid = log_dict[log_key]
        return [0, auid]

    def _wash_mf(self, log_key, log_dict):
        """
        wash mf,
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys() or log_dict[log_key] == "":
            return [-1, '%serr' % log_key]

        return [0, log_dict[log_key].replace(',', '')]


if __name__ == '__main__':
    start_time = sys.argv[1]
    mg_live_base_client = MgLiveBaseFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mg_live_base_client.processFormat(line)
        # print res[0]
        # print res[1]
