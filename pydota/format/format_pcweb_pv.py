#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format pcweb_pv class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
from format_base import FormatBase
from conf_settings import ServerConf


class PcWebPvFormat(FormatBase):
    """
    pcweb_pv
    """
    def __init__(self, recv_time, topic_name='pcweb_pv'):
        super(PcWebPvFormat, self).__init__(recv_time)
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


if __name__ == '__main__':
    start_time = sys.argv[1]
    pcweb_pv_client = PcWebPvFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = pcweb_pv_client.processFormat(line)
        # print res[0]
        # print res[1]