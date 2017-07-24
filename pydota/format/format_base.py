#!/usr/bin/env python
# encoding: utf-8
"""
Brief  : format base class
Author : guodong@mgtv.com
Date   : 2015.11.26
"""

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import string
from IPy import IP
from user_agents import parse

path = sys.path[0]


class FormatBase(object):
    """
    format 基类
    接口返回错误码中：
    0:正确清洗，写入des/orig
    -1:日志内容错误清洗，写入des_err/orig_err
    -3:不需要写入的错误，直接丢弃
    """

    def __init__(self, recv_time):
        """
        init fun
        :return:
        """
        self.name = "format_base"
        self.recv_time = recv_time
        self.input_log_num = 0
        self.output_log_num = 0
        self.err_log_num = 0
        self.drop_log_num = 0
        self.GEOIP_SORT = []
        self.GEOIP = {}
        self.des_key_list = []
        self.des_dict_list = []
        self.des_dict = {}
        self.file_list = {}
        self.loadGeoIp(os.path.join(os.path.dirname(__file__), "../geoip"))
        # self.write_to_file = write_to_file

    def loadGeoIp(self, filename):
        """
        :summery: 加载GEOIP库
        :param filename: GEOIP文件路径
        :return: 生成GEOIP相关dict
        """
        fp = open(filename)
        for i, line in enumerate(fp):
            try:
                record = string.split(line, "\t")
                rangmin  = record[0]
                rangmax  = record[1]
                country  = record[2]
                province = record[3]
                city     = record[4]
                operator = record[6]
                rangmin = IP(rangmin).int()
                rangmax = IP(rangmax).int()
                self.GEOIP[rangmin] = [rangmax, country, province, city, operator]
                self.GEOIP_SORT.append(rangmin)
            except ValueError:
                sys.stderr.write(("value error,%s") % line)
        self.GEOIP_SORT.sort()
        fp.close()

    def _getRangeKey(self, userip):
        list_len = len(self.GEOIP_SORT)
        low = 0
        height = list_len - 1
        while low <= height:
            mid = (low+height)/2
            if self.GEOIP_SORT[mid] <= userip and (mid == list_len - 1 or self.GEOIP_SORT[mid +1] > userip):
                return self.GEOIP_SORT[mid]
            elif low == height:
                return None
            elif self.GEOIP_SORT[mid + 1] <= userip:
                low = mid + 1
            elif self.GEOIP_SORT[mid] > userip:
                height = mid - 1
            else:
                return None
        return None

    def formatLocation(self, userip):
        """
        :summery: 根据userip获取地域信息
        :param userip: 用户ip 127.0.0.1
        :return: 地域信息list
        """
        userip = userip.strip('""')
        try:
            userip = IP(userip).int()
        except ValueError:
            return None
        location = self._getRangeKey(userip)
        if location and self.GEOIP[location]:
            if location <= userip <= self.GEOIP[location][0]:
                return self.GEOIP[location]
        else:
            return None

    def gen_des_dict(self, log_dict):
        """
        产生des的字典
        :return:
        """
        des_dict = {}
        for _k in self.des_dict_list:
            limit = self.des_dict[_k]
            if len(limit) not in [2, 3, 4]:
                return [-2, '%s config limit len not in [2,3,4], key:%s value:%s' % (self.name, _k, str(limit))]
            limit_type = limit[1]
            if isinstance(limit[0], str):
                log_key = limit[0]
            else:
                log_key = "%s.%s" % (limit[0][0], limit[0][1])
                if limit[0][0] in log_dict.keys():
                    log_dict[log_key] = log_dict[limit[0][0]].get(limit[0][1], '')
                else:
                    return [-1, "%serr" % log_key]
            if limit_type == 0:
                if log_key not in log_dict:
                    log_dict[log_key] = '-'
            elif limit_type == 1:
                if log_key not in log_dict.keys() or log_dict[log_key] == '':
                    return [-1, '%serr' % log_key]
            elif limit_type == 2:
                log_dict[log_key] = limit[2]
            elif limit_type == 3:
                limit_value = limit[2].split('|')
                match = False
                if log_key in log_dict:
                    for limit_value_tmp in limit_value:
                        if str(log_dict[log_key]) == limit_value_tmp:
                            match = True
                            break
                    if not match:
                        if len(limit) < 4:
                            return [-1, '%serr' % log_key]
                        else:
                            # -3表示该条错误不会落地到文件
                            return [-3, '']
                else:
                    return [-1, '%serr' % log_key]
            elif limit_type == 4:
                # 通过函数处理该字段
                result = self.runMyWash(_k, log_key, log_dict)
                if result[0] == 0:
                    des_dict[_k] = str(result[1])
                    continue
                else:
                    return result
            else:
                return [-2, "%s config limit_type error,key:%s value:%s" % (self.name, _k, str(limit))]
            des_dict[_k] = str(log_dict[log_key])
        return [0, des_dict]

    def gen_des_line(self, des_dict):
        """
        将des_dict拼接成des line
        :param des_dict: 清洗完成后的des字典
        :type des_dict: dict
        :return: string
        """
        diff_key = list(set(self.des_key_list).difference(set(des_dict)))
        if len(diff_key) != 0:
            return [-2, "topic_name:%s,des_dict not key:%s" % (self.name, str(diff_key))]
        result = ("{%s}" % ('},{'.join(self.des_key_list))).format(**des_dict)

        # 替换换行符
        return [0, result.replace('\n', '')]

    def runMyWash(self, des_key, log_key, log_dict):
        """
        获取对应的函数清洗
        :param des_key: des_dict中的字段名
        :type des_key: basestring
        :param log_key: 上报日志中，des_key对应的字段
        :type log_key: basestring
        :param log_dict: 上报日志字典
        :type log_dict: dict
        :return: [err_num, wash_value or errmsg]
        """
        fun_name = '_wash_%s' % des_key
        if hasattr(self, fun_name):
            wash_function = getattr(self, fun_name)
            return wash_function(log_key, log_dict)
        else:
            return [-2, "no function[%s] for %s " % (fun_name, log_key)]

    def getDictByLog(self, log_str):
        """
        通过日志获取Dict，子类必须重写该方法
        :param log_str:
        :return:
        """
        pass

    def getDictByUrl(self, content, _dict):
        """
        通过url获取dict
        :param content:
        :param _dict:
        :return:
        """
        if content == '' or content is None:
            return [-1, 'indexerr']
        _list = content.strip().split('?')
        if len(_list) < 2:
            return [-1, 'indexerr']
        arg_content = "?".join(_list[1:])
        for k_v in arg_content.split('&'):
            _l = k_v.split('=')
            if len(_l) != 2:
                continue
            (_k, _v) = _l
            _dict[_k] = _v
        return [0, '']

    def getDictByUrlNew(self, content, _dict):
        """
        通过url获取dict,新版,用于不含？
        :param content:
        :param _dict:
        :return:
        """
        if content == '' or content is None:
            return [-1, 'indexerr']
        for k_v in content.split('&'):
            _l = k_v.split('=')
            if len(_l) != 2:
                continue
            (_k, _v) = _l
            _dict[_k] = _v
        return [0, '']

    def getMobielVVUserAgent(self, content, _dict):
        if content == '' or content is None:
            return [0, 'no_cache']

        user_agent = parse(content)

        os_f = user_agent.os.family
        version_str = user_agent.os.version_string
        mf = user_agent.device.brand
        mod = user_agent.device.model

        if version_str == "":
            os_str = os_f
        else:
            os_str = str(os_f) + "-" + str(version_str)

        _dict["os"] = str(os_str)

        if "generic" in str(mf).lower() or "none" in str(mf).lower():
            if "none" in str(mod).lower() or "smartphone" in str(mod).lower():
                return [0, 'no_cache']

            if 'mf' in _dict and _dict['mf'] != "":
                mf = str(_dict['mf'])
            else:
                mf = 'Unknown'

            # if 'mod' in _dict and _dict['mod'] != "":
            #     mod = str(_dict['mod'])

        _dict["mf"] = str(mf)
        _dict["mod"] = str(mod)

        return [0, '']

    def getVersionNum(self, content):
        """
        获取版本数
        :param content:
        :return:
        """
        _list = content.split('-')
        if len(_list) < 3:
            _list = content.split('_')
        if len(_list) < 3:
            return [-1, 'versionNumerr']
        ver = ''.join(_list[2].split('.')[0:3])
        ver = str(ver)[0:3]
        if ver.isdigit():
            return [0, int(ver)]
        else:
            return [-1, 'versionNumerr']

    def _wash_tid(self, log_key, log_dict):
        """
        wash tid, ',' 替换为 '-'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        return [0, log_dict[log_key].replace(',', '_')]

    def _wash_ref(self, log_key, log_dict):
        """
        wash ref, ','去掉
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]

        return [0, urllib.unquote(log_dict[log_key]).replace(',', '')]

    def _wash_cookie(self, log_key, log_dict):
        """
        wash cookie, 转小写
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys() or log_dict[log_key] == "":
            return [-1, '%serr' % log_key]
        return [0, str(log_dict[log_key]).lower()]

    def _wash_date(self, log_key, log_dict):
        """
        wash date, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]
        return [0, str(log_dict[log_key])[0:8]]

    def _wash_time(self, log_key, log_dict):
        """
        wash time, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]
        return [0, str(log_dict[log_key])[8:]]

    def _wash_province(self, log_key, log_dict):
        """
        wash province, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]
        locationtmp = self.formatLocation(str(log_dict[log_key]))
        if locationtmp is None or len(locationtmp) <= 2:
            return [-1, 'locationerr']
        return [0, locationtmp[2]]

    def _wash_country(self, log_key, log_dict):
        """
        wash country, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]
        locationtmp = self.formatLocation(str(log_dict[log_key]))
        if locationtmp is None or len(locationtmp) <= 2:
            return [-1, 'locationerr']
        return [0, locationtmp[1]]

    def _wash_isp(self, log_key, log_dict):
        """
        wash 运营商, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]
        locationtmp = self.formatLocation(str(log_dict[log_key]))
        if locationtmp is None or len(locationtmp) <= 4:
            return [-1, 'locationerr']
        return [0, locationtmp[4]]

    def _wash_city(self, log_key, log_dict):
        """
        wash city, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [-1, '%serr' % log_key]
        locationtmp = self.formatLocation(str(log_dict[log_key]))
        if locationtmp is None or len(locationtmp) <= 3:
            return [-1, 'locationerr']
        return [0, locationtmp[3]]

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
        if 'apad' in value:
            tp = 'apad'
        elif 'ipad' in value:
            tp = 'ipad'
        elif 'aphone' in value:
            tp = 'android'
        elif 'iphone' in value:
            tp = 'iphone'
        else:
            return [-1, 'clienttperr']
        return [0, tp]

    def _wash_clientver(self, log_key, log_dict):
        """
        wash clientver, 转小写
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys() or log_dict[log_key] == "":
            return [-1, '%serr' % log_key]
        return [0, str(log_dict[log_key]).lower()]

    def _wash_ln(self, log_key, log_dict):
        """
        wash ln, 进行url解码
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        return [0, urllib.unquote(log_dict[log_key])]

    def _wash_url(self, log_key, log_dict):
        """
        wash url, ','去掉
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]

        return [0, urllib.unquote(log_dict[log_key]).replace(',', '')]

    def _wash_ch(self, log_key, log_dict):
        """
        wash ch, 转小写
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).lower()]

    def _wash_manufacturers(self, log_key, log_dict):
        """
        wash manufacturers, 转小写
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]

        return [0, urllib.unquote(log_dict[log_key]).replace(',', '')]

    def _wash_mf(self, log_key, log_dict):
        """
        wash mf,
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]

        return [0, log_dict[log_key].replace(',', '')]

    def _wash_mod(self, log_key, log_dict):
        """
        wash mod,
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]

        return [0, log_dict[log_key].replace(',', '-')]

    def _wash_fpa(self, log_key, log_dict):
        """
        wash fpa, ',' 替换为 '|'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).replace(',', '|')]

    def _wash_cma(self, log_key, log_dict):
        """
        wash cma, ',' 替换为 '|'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).replace(',', '|')]

    def _wash_cid(self, log_key, log_dict):
        """
        wash cid, ',' 替换为 '|'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).replace(',', '|')]

    def _wash_fpid(self, log_key, log_dict):
        """
        wash fpid, ',' 替换为 '|'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).replace(',', '|')]

    def _wash_cpid(self, log_key, log_dict):
        """
        wash cpid, ',' 替换为 '|'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).replace(',', '|')]

    def _wash_frompageid(self, log_key, log_dict):
        """
        wash frompageid, ',' 替换为 '|'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).replace(',', '|')]

    def _wash_currentpageid(self, log_key, log_dict):
        """
        wash currentpageid, ',' 替换为 '|'
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if log_key not in log_dict.keys():
            return [0, '-']
        if log_dict[log_key] == "":
            return [0, ""]
        return [0, str(log_dict[log_key]).replace(',', '|')]

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

        _res_result = self.gen_des_line(_res_des[1])
        if _res_result[0] == 0:
            if len(self.des_key_list) == len(str(_res_result[1]).split(',')):
                self.output_log_num += 1
                # self.write_to_file(_res_result[1], self.name, log_time, self.recv_time, 'des')
                return [0, _res_result[1], log_time]
            else:
                self.err_log_num += 1
                # self.write_to_file('record_col_err,%s' % _res_result[1], self.name, log_time, self.recv_time, 'des_err')
                return [-2, 'record_col_err,%s' % _res_result[1], log_time]
        else:
            self.drop_log_num += 1
            return [-3, '', log_time]
        # return self.gen_des_line(_res_des[1])