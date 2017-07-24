#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format ott_live class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf


class OttLiveFormat(FormatBase):
    """
    ott_live
    """
    def __init__(self, recv_time, topic_name='ott_live'):
        super(OttLiveFormat, self).__init__(recv_time)
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
        if len(log_str.strip('\n')) == 0:
            return [-1, "recorderr"]

        try:
            _dict_tmp = json.loads(log_str)
            if 'play_realtime' in _dict_tmp.keys():
                _dict = _dict_tmp['play_realtime']
                _dict['time'] = str(_dict['date']) + str(_dict['index_record'])
                return [0, _dict]
            else:
                return [-1, 'playrealtimeerr']
        except (ValueError, KeyError):
            return [-1, 'jsonerr']


if __name__ == '__main__':
    start_time = sys.argv[1]
    ott_live_client = OttLiveFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = ott_live_client.processFormat(line)
        # print res[0]
        # print res[1]
