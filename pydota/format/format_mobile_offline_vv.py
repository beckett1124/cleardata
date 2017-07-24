#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mobile_offline_vv class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import json
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common_new import write_to_file


class MobileOffLineVVFormat(FormatBase):
    """
    mobile_offline_vv
    """
    def __init__(self, recv_time, topic_name='mobile_offline_vv'):
        super(MobileOffLineVVFormat, self).__init__(recv_time)
        self.name = topic_name
        self.log_all_list = []
        self.ua_content_dict = {}
        self.des_key_list = ServerConf[self.name]["des_key_list"]
        self.des_dict_list = ServerConf[self.name]["des_dict_list"]
        self.des_dict = ServerConf[self.name]["des_dict"]
        self.write_to_file = write_to_file

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

        md_log_str = str(_dict.get('mod', "")).strip()

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

        if "iphone" in str(_dict.get('aver', '')).lower():
            _dict['mod'] = md_log_str

        return [0, _dict]

    def fix_os(self, os_str):
        if str(os_str).endswith(".0"):
            return str(os_str)[0:len(os_str)-2]
        else:
            return str(os_str)

    def _wash_act(self, log_key, log_dict):
        """
        wash act, 必须为aplay，aplay替换为play
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]

        # 非alay事件直接丢弃,-3
        if log_dict[log_key] != "aplay":
            return [-3, '']
        return [0, "play"]

    def processFormat(self, content):
        """
        清洗主程序 offline
        :param content: 原始日志
        :type content: basestring
        :return:
        """
        if content is None or content == '':
            return [99, '']
        _res = self.getDictByLog(content)

        if _res[0] == -1:
            self.input_log_num += 1
            self.err_log_num += 1

            self.write_to_file('%s,%s' % (_res[1], content), self.name, self.recv_time, self.recv_time, 'orig_err')
            # return _res
            return [99, '']

        try:
            log_time = _res[1]['time'][0:10] + "00"
        except(ValueError, TypeError, KeyError):
            self.input_log_num += 1
            self.err_log_num += 1

            self.write_to_file('timeerr,%s' % content, self.name, self.recv_time, self.recv_time, 'orig_err')
            return [99, '']

        # 是否加list的长度
        self.input_log_num += len(self.log_all_list)
        self.write_to_file(content, self.name, log_time, self.recv_time, 'orig')

        if _res[0] == -3:
            self.drop_log_num += 1
            return [99, '']

        for log_dict in self.log_all_list:
            log_dict['ip'] = _res[1]['ip']
            log_dict['time'] = _res[1]['time']
            if 'os' in _res[1]:
                log_dict['os'] = _res[1]['os']
            if 'mf' in _res[1]:
                log_dict['mf'] = _res[1]['mf']
            if 'mod' in _res[1]:
                log_dict['mod'] = _res[1]['mod']

            # net = ""
            # if "net" in log_dict.keys():
            #     net = log_dict["net"]

            _res_des = self.gen_des_dict(log_dict)
            if _res_des[0] == -1:
                self.err_log_num += 1
                self.write_to_file('%s,%s' % (_res_des[1], log_dict), self.name, log_time, self.recv_time, 'des_err')
                # return _res_des
                continue
            elif _res_des[0] != 0:
                self.drop_log_num += 1
                # return _res_des
                continue

            # android pt=3 net=0的数据另写文件，待校验通过后，再合并
            topic_name = self.name
            # if isinstance(_res_des[1], dict):
            #     clienttp = _res_des[1].get("clienttp")
            #     pt = _res_des[1].get("pt")
            #
            #     if clienttp is None or pt is None:
            #         pass
            #     elif clienttp != "iphone" and str(pt) == "3" and str(net) == "0":
            #         topic_name = "android_offline_vv"

            _res_result = self.gen_des_line(_res_des[1])
            if _res_result[0] == 0:
                if len(self.des_key_list) == len(str(_res_result[1]).split(',')):
                    self.output_log_num += 1
                    self.write_to_file(_res_result[1], topic_name, log_time, self.recv_time, 'des')
                else:
                    self.err_log_num += 1
                    self.write_to_file('record_col_err,%s' % _res_result[1], self.name, log_time, self.recv_time, 'des_err')
                    continue
            else:
                self.drop_log_num += 1

        return [99, '']
        # return self.gen_des_line(_res_des[1])

if __name__ == '__main__':
    start_time = sys.argv[1]
    mobile_offline_vv_client = MobileOffLineVVFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mobile_offline_vv_client.processFormat(line)
        # print res[0]
        # print res[1]
