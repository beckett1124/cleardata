#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format ott_vv_41 class
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


class OttVV41Format(FormatBase):
    """
    ott_vv_41
    """
    def __init__(self, recv_time, topic_name='ott_vv_41'):
        super(OttVV41Format, self).__init__(recv_time)
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

    def _wash_cookie(self, log_key, log_dict):
        """
        wash cookie, 转小写
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if "apk_version" not in log_dict.keys() or log_dict["apk_version"] == "":
            return [-1, 'apk_versionerr']
        apk_ver_list = str(log_dict["apk_version"]).lower().split(".")

        if len(apk_ver_list) >= 6 and apk_ver_list[5] == "sx":
            if "mac" not in log_dict.keys() or log_dict["mac"] == "":
                return [-1, 'macerr']
            cookie = str(log_dict["mac"]).lower()
        else:
            if log_key not in log_dict.keys() or log_dict[log_key] == "":
                return [-1, '%serr' % log_key]
            cookie = str(log_dict[log_key])
        return [0, cookie]

    def _wash_url(self, log_key, log_dict):
        """
        wash url, ','去掉
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, "%serr" % log_key]

        vid_url = urllib.unquote(log_dict[log_key]).replace(',', '')

        index_url = str(vid_url).lower().find("internettv")
        if index_url == -1:
            return [-1, "play_urlerr"]
        else:
            play_url = vid_url[index_url+len("internettv"):]
            index_ts = play_url.find("?")
            if index_ts >= 0:
                play_url = play_url[0:index_ts]

        if str(play_url) == "":
            return [-1, "play_urlerr"]

        return [0, play_url]


if __name__ == '__main__':
    start_time = sys.argv[1]
    ott_vv_41_client = OttVV41Format(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = ott_vv_41_client.processFormat(line)
        # print res[0]
        # print res[1]
