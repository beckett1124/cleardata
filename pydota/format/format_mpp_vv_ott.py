#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mpp_vv_ott class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import time
import json
import urllib
from format_base import FormatBase
from conf_settings import ServerConf


class MppVVOttFormat(FormatBase):
    """
    mpp_vv_mobile_ott
    """
    def __init__(self, recv_time, topic_name='mpp_vv_ott'):
        super(MppVVOttFormat, self).__init__(recv_time)
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
            _dict = json.loads(log_str)
        except ValueError:
            return [-1, 'jsonerr']

        try:
            time_tmp = float(_dict['time'])
            time_data = time.localtime(time_tmp)
            _dict['time'] = time.strftime('%Y%m%d%H%M%S', time_data)
        except (ValueError, KeyError):
            return [-1, 'timeerr']

        return [0, _dict]

    def _wash_vid(self, log_key, log_dict):
        """
        wash vid
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, "%serr" % log_key]

        vid_url = urllib.unquote(log_dict[log_key]).replace(',', '')

        index_url = str(vid_url).lower().find("internettv")
        if index_url == -1:
            return [-1, "viderr"]
        else:
            vid = vid_url[index_url+len("internettv"):]
            index_ts = str(vid).lower().find("?")
            if index_ts >= 0:
                vid = vid[0:index_ts]

        if str(vid) == "":
            return [-1, "viderr"]

        return [0, vid]

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
    mpp_vv_ott_client = MppVVOttFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mpp_vv_ott_client.processFormat(line)
        # print res[0]
        # print res[1]
