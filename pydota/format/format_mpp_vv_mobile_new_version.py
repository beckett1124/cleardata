#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mobile_new_version class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common import check_act_field


class MppVVMobileNewVersionFormat(FormatBase):
    """
    mpp_vv_mobile_new_version
    """
    def __init__(self, recv_time, topic_name='mpp_vv_mobile_new_version'):
        super(MppVVMobileNewVersionFormat, self).__init__(recv_time)
        self.name = topic_name
        self.log_all_list = []
        self.ua_content_dict = {}
        self.des_key_list = ServerConf[self.name]["des_key_list"]
        self.des_dict_list = ServerConf[self.name]["des_dict_list"]
        self.des_dict = ServerConf[self.name]["des_dict"]

    def getDictByLog(self, log_str):
        """
        通过日志获取Dict
        :param log_str:
        :return:
        """
        self.log_all_list = []
        res_list = log_str.strip().split('\t')
        if len(res_list) < 8:
            return [-1, "indexerr"]
        json_content = res_list[7].strip()

        _dict = dict()
        _dict['ip'] = res_list[1]
        _dict['time'] = res_list[0]

        if not check_act_field(json_content, "play", "aplay"):
            return [-3, _dict]

        try:
            _list = json.loads(json_content)
            if isinstance(_list, dict):
                _dict = _list
                self.log_all_list.append(_dict)
            elif isinstance(_list, list):
                _dict = _list[0]
                self.log_all_list = _list
            else:
                return [-1, 'jsonerr']
        except ValueError:
            return [-1, 'jsonerr']

        _dict['ip'] = res_list[1]
        _dict['time'] = res_list[0]

        ua_content = res_list[4].strip()

        if 'mod' in _dict and _dict['mod'] != "":
            md_list = str(_dict['mod']).strip().split(' ')
            if len(md_list) > 1:
                md_str = ' '.join(md_list[1:])
            else:
                md_str = str(md_list[0])
            _dict['mod'] = md_str
        else:
            _dict['mod'] = ""

        if 'sver' in _dict and _dict['sver'] != "":
            os_str = str(_dict['sver']).lower()
            if "iphone" in os_str:
                os_str = os_str.replace('iphone', 'iOS')
            elif "ipad" in os_str:
                os_str = os_str.replace('ipad', 'iOS')
            elif "aphone" in os_str:
                os_str = os_str.replace('aphone', 'Android')
            elif "aos" in os_str:
                os_str = os_str.replace('aos', 'Android')

            _dict['os'] = self.fix_os(os_str)
        else:
            _dict['os'] = ""

        if str(ua_content) == "":
            return [0, _dict]

        browser_ver_os_list = self.ua_content_dict.get(ua_content)
        if browser_ver_os_list is None:
            res_ua = self.getMobielVVUserAgent(ua_content, _dict)
            if res_ua[1] == "no_cache":
                self.ua_content_dict[ua_content] = []
                return [0, _dict]

            if 'os' in _dict and 'mf' in _dict and 'mod' in _dict:
                self.ua_content_dict[ua_content] = [_dict['os'], _dict['mf'], _dict['mod']]
            else:
                self.ua_content_dict[ua_content] = []
        else:
            if isinstance(browser_ver_os_list, list) and len(browser_ver_os_list) >= 3:
                _dict['os'] = browser_ver_os_list[0]
                _dict['mf'] = browser_ver_os_list[1]
                _dict['mod'] = browser_ver_os_list[2]

        return [0, _dict]

    def fix_os(self, os_str):
        if str(os_str).endswith(".0"):
            return str(os_str)[0:len(os_str)-2]
        else:
            return str(os_str)

    def _wash_act(self, log_key, log_dict):
        """
        wash act, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            _act = ''
        else:
            _act = log_dict[log_key]

        if "aver" not in log_dict.keys():
            return [-1, 'avererr']
        _ver = log_dict["aver"]
        ver = _ver.lower()
        pro_ver = ''
        if 'imgotv_iphone' in ver:
            res_tmp = self.getVersionNum(ver)
            if res_tmp[0] != 0:
                return res_tmp
            if 450 <= res_tmp[1] <= 453:
                pro_ver = 'iphone450453'
            elif res_tmp[1] >= 454:
                pro_ver = 'iphone454'
            else:
                pro_ver = ''
        elif 'imgotv_aphone' in ver:
            res_tmp = self.getVersionNum(ver)
            if res_tmp[0] != 0:
                return res_tmp
            if res_tmp[1] >= 452:
                pro_ver = 'aphone452'
        elif str(ver).startswith('aphone'):
            pro_ver = 'aphoneother'
        elif ver == '4.5.2':
            pro_ver = 'aphone452'

        if pro_ver in ['aphone452', 'iphone454']:
            if _act == 'aplay':
                return [0, 'play']
            else:
                return [-3, 'not aplay']
        elif pro_ver in ['iphone450453', 'aphoneother']:
            for i in range(len(self.log_all_list)):
                if self.log_all_list[i].get('act', '') == 'play':
                    return [0, 'play']
            return [-3, 'not play']
        else:
            if _act == 'aplay':
                return [0, 'play']
        return [-1, '%serr' % log_key]

    def _wash_clienttp(self, log_key, log_dict):
        """
        wash clienttp,
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys() or log_dict[log_key] == "":
            return [-1, '%serr' % log_key]
        value = str(log_dict[log_key]).lower()
        if 'iphone' in value:
            tp = 'iphone'
        else:
            tp = 'android'
        return [0, tp]

if __name__ == '__main__':
    start_time = sys.argv[1]
    mobile_new_version_client = MppVVMobileNewVersionFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mobile_new_version_client.processFormat(line)
        # print res[0]
        # print res[1]
