#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mpp_vv_mobile class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import time
import json
from format_base import FormatBase
from conf_settings import ServerConf


class MppVVMobileFormat(FormatBase):
    """
    mpp_vv_mobile_new_version
    """
    def __init__(self, recv_time, topic_name='mpp_vv_mobile'):
        super(MppVVMobileFormat, self).__init__(recv_time)
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
            time_tmp = _dict['time']
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
        if log_key not in log_dict.keys():
            return [-1, "%serr" % log_key]
        clientver = str(log_dict[log_key]).lower()
        if clientver == '4.5.2':
            # 4.5.2在new_version中清洗，旧版中丢弃
            return [-1, "clientvererr"]
        if clientver == "imgotv_aphone_45000":
            pass
        elif "aphone" in clientver:
            version = self.getVersionNum(clientver)
            if version[0] != 0:
                return version
            if version[1] <= 0 or version[1] >= 452:
                return [-1, 'versionNumerr']
        elif "iphone" in clientver:
            version = self.getVersionNum(clientver)
            if version[0] != 0:
                return version
            if version[1] <= 0 or version[1] >= 450:
                return [-1, 'versionNumerr']

        return [0, clientver]

    def _wash_mod(self, log_key, log_dict):
        """
        wash mod
        :param log_key:
        :param log_dict:
        :return:
        """
        key_list = str(log_key).split("|")
        if len(key_list) < 2:
            return [-1, 'mod_input_err']

        if key_list[0] not in log_dict or key_list[1] not in log_dict:
            return [0, '']

        model = str(log_dict[key_list[0]]).lower()
        apk_version = str(log_dict[key_list[1]]).lower()

        if model == "":
            return [0, ""]

        if "ipad" in apk_version or "iphone" in apk_version:
            model = model
        else:
            model_list = model.split(" ")
            if len(model_list) > 1:
                model = ' '.join(model_list[1:])

        return [0, model]

    def _wash_mf(self, log_key, log_dict):
        """
        wash mod
        :param log_key:
        :param log_dict:
        :return:
        """
        key_list = str(log_key).split("|")
        if len(key_list) < 2:
            return [-1, 'mod_input_err']

        if key_list[0] not in log_dict or key_list[1] not in log_dict:
            return [0, '']

        model = str(log_dict[key_list[0]]).lower()
        apk_version = str(log_dict[key_list[1]]).lower()

        if model == "":
            return [0, ""]

        if "ipad" in apk_version or "iphone" in apk_version:
            mf = "apple"
        else:
            model_list = model.split(" ")
            if len(model_list) > 1:
                mf = model_list[0]
            else:
                mf = "Unknown"

        return [0, mf]

    def _wash_os(self, log_key, log_dict):
        """
        wash mod
        :param log_key:
        :param log_dict:
        :return:
        """
        key_list = str(log_key).split("|")
        if len(key_list) < 2:
            return [-1, 'os_input_err']

        if key_list[0] not in log_dict or key_list[1] not in log_dict:
            return [0, '']

        sys_version = str(log_dict[key_list[0]]).lower()
        apk_version = str(log_dict[key_list[1]]).lower()

        if sys_version == "":
            return [0, ""]

        try:
            sys_version_nu = float(sys_version)
            sys_version = str([str(sys_version_nu), int(sys_version_nu)][int(sys_version_nu) == sys_version_nu])
        except ValueError:
            sys_version = sys_version

        if "ipad" in apk_version or "iphone" in apk_version:
            os = "ios-" + sys_version
        else:
            os = "android-" + sys_version

        return [0, os]


if __name__ == '__main__':
    start_time = sys.argv[1]
    mpp_vv_mobile_client = MppVVMobileFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mpp_vv_mobile_client.processFormat(line)
        # print res[0]
        # print res[1]
