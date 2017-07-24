#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mpp_vv_padweb class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import urllib
from format_base import FormatBase
from conf_settings import ServerConf


class MppVVPadWebFormat(FormatBase):
    """
    mpp_vv_padweb
    """
    def __init__(self, recv_time, topic_name='mpp_vv_padweb'):
        super(MppVVPadWebFormat, self).__init__(recv_time)
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
        url_content = res_list[7]
        res_tmp = self.getDictByUrlNew(url_content, _dict)

        if res_tmp[0] != 0:
            return res_tmp
        _dict['ip'] = res_list[1]
        _dict['time'] = res_list[0]

        return [0, _dict]

    def _wash_tid(self, log_key, log_dict):
        """
        wash tid, ',' 替换为 '_', 进行url解码
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        return [0, urllib.unquote(log_dict[log_key]).replace(',', '_')]


if __name__ == '__main__':
    start_time = sys.argv[1]
    mpp_vv_padweb_client = MppVVPadWebFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mpp_vv_padweb_client.processFormat(line)
        # print res[0]
        # print res[1]
