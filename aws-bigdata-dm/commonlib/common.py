# encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-17T21:19:51+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T11:47:09+08:00

import ConfigParser
import re
import os
import time
import urllib
from conf.settings import AppConfig
from commonlib.pydotalog import pydotalog


file_list = {}

regex_zn = "^(http|https)://([0-z]+.)?(mgtv|hunantv|imgo).(com|tv)"
pattern_zn = re.compile(regex_zn)


def CheckLiveTime(log_time,live_info=[]):
    """
    :check log time is effect,if this time effect return action id and cameraid
    """
    for live_info_one in live_info:
        try:
            startTime=time.strptime(live_info_one[3],"%Y-%m-%d %H:%M:%S")
            endTime=time.strptime(live_info_one[4],"%Y-%m-%d %H:%M:%S")

            startTime=int(time.mktime(startTime))
            endTime=int(time.mktime(endTime))

            if startTime <= int(log_time) <= endTime:
                return 0,live_info_one[0],live_info_one[1]
            else:
                continue

        except (KeyError,ValueError) as e:
            pydotalog.error("check time failed:%s",str(e))
            return -1,0,0

    pydotalog.error("%s is not a valid time!",str(log_time))
    return -2,0,0


def formatTime(timedata):
    """
    :format time
    """
    try:
        timetmp_date=time.strftime('%Y%m%d',timedata)
        timetmp_time=time.strftime('%H%M%S',timedata)
        timeStamp=int(time.mktime(timedata))
    except (ValueError,TypeError):
        raise ValueError("timeerr")


def __genOutputFileName(log_time,topic,start_time,data_type):
    """
    :write file
    """
    try:
        output_path = AppConfig['data_out_put'][data_type]
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
        pydotalog.error("initConfig fail:%s", str(e))
        return ""

    dir_name = '{0}/{1}/{2}/{3}/{4}/{5}'.format(str(output_path), topic, log_time[0:4], log_time[4:6],
                                                log_time[6:8], log_time[8:10])

    if "err" in data_type:
        file_str = '{0}/err_{1}_{2}_{3}'.format(str(dir_name), log_time, topic, start_time)
    elif "des" == data_type:
            file_str = '{0}/{1}_dm_{2}_{3}'.format(str(dir_name), log_time, topic, start_time)
    else:
        file_str = '{0}/{1}_{2}_{3}'.format(str(output_path), log_time, topic, start_time)
    file_str = os.path.abspath(file_str)
    dir_name = os.path.dirname(file_str)

    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as e:
            pydotalog.error("make dir failed:[%s]", str(e))
            return ""
    return file_str


def __output_to_files(log_time, line, topic, start_time, data_type):
    str_log_file = __genOutputFileName(log_time, topic, start_time, data_type)

    if str_log_file == "":
        return False

    if str_log_file in file_list:
        log_file = file_list[str_log_file]
    else:
        try:
            log_file = open(str_log_file, 'w')
            file_list[str_log_file] = log_file
        except IOError as e:
            pydotalog.error("IOError: %s", str(e))
            return False

    log_file.write(line.strip('\n') + '\n')
    return True


def __check_time(log_time):
    if len(log_time) != 10:
        return False
    try:
        return 2010000000 < int(log_time) < 2050000000
    except ValueError:
        pydotalog.error("log_time[%s] is overtime", str(log_time))
        return False


def write_to_file(line, topic, log_time, start_time, data_type):

    if __check_time(log_time):
        return __output_to_files(log_time, line, topic, start_time, data_type)
    else:
        return False


def check_act_field(line, *args):
    if len(line.strip('\n')) == 0 or len(args) == 0:
        return False
    for arg in args:
        act_str = '"act":"' + str(arg) + '"'
        if line.find(act_str) != -1:
            return True

    return False


def check_pt_field(line, *args):
    if len(line.strip('\n')) == 0 or len(args) == 0:
        return False
    for arg in args:
        act_str = '"pt":"' + str(arg) + '"'
        act_str1 = '"pt":' + str(arg)
        if line.find(act_str) != -1 or line.find(act_str1) != -1:
            return True

    return False


def ip_into_int(ip):
    # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
    # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
    try:
        ip_int = reduce(lambda x, y: (x << 8)+y, map(int, ip.split('.')))
    except ValueError:
        return 0
    return ip_int


def is_internal_ip(ip):
    if str(ip) == "127.0.0.1":
        return True

    ip = ip_into_int(ip)

    # 无效ip统一当内网ip透传
    if ip == 0:
        return False
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c


def get_version_num(content):
    """
    获取版本数
    :param content:
    :return:
    """
    _list = content.split('-')
    if len(_list) < 3:
        _list = content.split('_')
    if len(_list) < 3:
        return [1, 'versionNumerr']
    ver = ''.join(_list[2].split('.')[0:3])
    ver = str(ver)[0:3]
    if ver.isdigit():
        return [0, int(ver)]
    else:
        return [1, 'versionNumerr']


def resolve_url(url_input):
    if str(url_input) == "" or str(url_input) == "-":
            return [0, url_input]

    try:
        url_str = urllib.unquote(url_input).decode('utf8')
    except UnicodeDecodeError:
        try:
            url_str = urllib.unquote(url_input).decode('gbk')
        except UnicodeDecodeError:
            return [1, "URL_DECODE_ERR"]

    url_tmp = str(url_str).replace(":80/", "/")

    if url_tmp.endswith(":80"):
        url_tmp = str(url_input).replace(":80", "")

    return [0, url_tmp]


def is_mg_vod(input_cpn):
    mg_vod_list = ["3", "5", "6", "81", "83"]
    if input_cpn is None:
        return False

    if str(input_cpn) in mg_vod_list:
        return True
    else:
        return False


def is_mg_url(url_str):
    # url为空 或者 不以http开头的,均算为站内，非第三方站点
    if str(url_str) == "" or not str(url_str).startswith("http"):
        return True

    match = pattern_zn.match(url_str)

    if match:
        return True
    else:
        return False

