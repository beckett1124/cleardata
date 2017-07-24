#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format mpp_vv_pcclient class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import sys
import fileinput
import time
from format_base import FormatBase
from conf_settings import ServerConf
from pydota_common import is_internal_ip
from pydota_common_new import write_to_file


class MppVVPcClientFormat(FormatBase):
    """
    mpp_vv_pcclient
    """
    def __init__(self, recv_time, topic_name='mpp_vv_pcclient'):
        super(MppVVPcClientFormat, self).__init__(recv_time)
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

    def _wash_pt(self, log_key, log_dict):
        """
        wash pt
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, "0"]
        pt = str(log_dict[log_key])
        if pt != "0":
            return [-1, "%serr" % log_key]
        return [0, pt]

    def processFormat(self, content):
        """
        清洗主程序
        :param content: 原始日志
        :type content: basestring
        :return:
        """
        if content is None or content == '':
            return [-3, '', self.recv_time]
        _res = self.getDictByLog(content)

        if _res[0] == -1:
            self.input_log_num += 1
            self.err_log_num += 1

            # self.write_to_file('%s,%s' % (_res[1], content), self.name, self.recv_time, self.recv_time, 'orig_err')
            # return _res
            return [-1, '%s,%s' % (_res[1], content), self.recv_time]

        try:
            log_time = _res[1]['time'][0:10] + "00"
        except(ValueError, TypeError, KeyError):
            self.input_log_num += 1
            self.err_log_num += 1

            # self.write_to_file('timeerr,%s' % content, self.name, self.recv_time, self.recv_time, 'orig_err')
            return [-1, 'timeerr,%s' % content, self.recv_time]

        self.input_log_num += 1
        # self.write_to_file(content, self.name, log_time, self.recv_time, 'orig')

        if _res[0] == -3:
            self.drop_log_num += 1
            return [-3, '', log_time]

        _res_des = self.gen_des_dict(_res[1])
        if _res_des[0] == -1:
            self.err_log_num += 1
            # self.write_to_file('%s,%s' % (_res_des[1], content), self.name, log_time, self.recv_time, 'des_err')
            # return _res_des
            return [-2, '%s,%s' % (_res_des[1], content), log_time]
        elif _res_des[0] != 0:
            self.drop_log_num += 1
            # return _res_des
            return [-3, '', log_time]

        pt = 0
        if isinstance(_res_des[1], dict):
            pt = _res_des[1].get("pt")

            if pt is None:
                pass

        _res_result = self.gen_des_line(_res_des[1])
        if _res_result[0] == 0:
            if len(self.des_key_list) == len(str(_res_result[1]).split(',')):
                self.output_log_num += 1
                if str(pt) == "5":
                    write_to_file(_res_result[1], "pcclient_offline_vv", log_time, self.recv_time, 'des')
                    return [99, '']
                return [0, _res_result[1], log_time]
            else:
                self.err_log_num += 1
                return [-2, 'record_col_err,%s' % _res_result[1], log_time]
        else:
            self.drop_log_num += 1
            return [-3, '', log_time]
        # return self.gen_des_line(_res_des[1])


if __name__ == '__main__':
    start_time = sys.argv[1]
    mpp_vv_pcclient_client = MppVVPcClientFormat(start_time)
    for line in fileinput.input(sys.argv[2:]):
        res = mpp_vv_pcclient_client.processFormat(line)
        # print res[0]
        # print res[1]
