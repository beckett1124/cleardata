#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format macclient_live_8111_20160105 class
Author : guodong@mgtv.com
Date   : 2016.01.05
"""

import sys
import fileinput
from format_base import FormatBase
from conf_settings import ServerConf


class MacClientLiveFormat(FormatBase):
    """
    macclient_live_8111_20160105
    """
    def __init__(self, recv_time, topic_name='macclient_live_8111_20160105'):
        super(MacClientLiveFormat, self).__init__(recv_time)
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

    def _wash_act(self, log_key, log_dict):
        """
        wash act, 必须为play，非play丢弃
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]

        # 非alay事件直接丢弃,-3
        if log_dict[log_key] != "play":
            return [-3, '']
        return [0, "play"]


if __name__ == '__main__':
    start_time = sys.argv[1]
    macclient_live_client = MacClientLiveFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = macclient_live_client.processFormat(line)
        # print res[0]
        # print res[1]
