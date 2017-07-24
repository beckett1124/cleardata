#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import os
from pydota.format.conf_settings import ServerConf
from pydota.commonlib.pydotalog import pydotalog

file_list = {}


def __genOutputFileName(log_time, topic, start_time, data_type, postfix):
    """
    根据日志时间，topic，后缀，数据类型拼接写入文件
    :param log_time: 需要写入的日志时间,精确到小时
    :type log_time: basestring 201511012200 12位
    :param topic: kafka－topic名称
    :type topic: basestring
    :param start_time: 文件后缀名称, 为recv文件的时刻
    :type start_time: basestring 201511012300 12位
    :param data_type: 写入数据的类型，分为 orig,des,err
    :type data_type: basestring
    :return:
    """
    output_path = ServerConf["output_path"][data_type]
    if output_path == "":
        pydotalog.error("initConfig fail: no key[output_path or %s]", data_type)
        return ""


    dir_name = '{0}/{1}/{2}'.format(str(output_path), log_time[0:4], log_time[4:6])

    if "err" in data_type:
        file_str = '{0}/err_{1}_{2}_{3}_{4}{5}'.format(dir_name, log_time, topic, start_time, data_type, postfix)
    elif "des" == data_type:
        if "_pv" in topic:
            file_str = '{0}/{1}_pvrawdata_{2}_{3}{4}'.format(dir_name, log_time, topic, start_time, postfix)
        elif "mglive" in topic:
            file_str = '{0}/{1}_mgliverawdata_{2}_{3}{4}'.format(dir_name, log_time, topic, start_time, postfix)
        elif "dau_" in topic:
            file_str = '{0}/{1}_daurawdata_{2}_{3}{4}'.format(dir_name, log_time, topic, start_time, postfix)
        else:
            file_str = '{0}/{1}_playrawdata_{2}_{3}{4}'.format(dir_name, log_time, topic, start_time, postfix)
    else:
        file_str = '{0}/{1}_{2}_{3}{4}'.format(dir_name, log_time, topic, start_time, postfix)

    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as e:
            pydotalog.error("make dir failed:[%s]", str(e))
            return ""
    return file_str


def __output_to_files(log_time, line, topic, start_time, data_type, postfix):
    str_log_file = __genOutputFileName(log_time, topic, start_time, data_type, postfix)

    if str_log_file == "":
        return False

    if str_log_file in file_list.keys():
        log_file = file_list[str_log_file]
    else:
        try:
            log_file = open(str_log_file, 'w')
            file_list[str_log_file] = log_file
        except IOError as e:
            pydotalog.error("IOError: %s", str(e))
            return False

    log_file.write(line.strip('\n') + '\n')
    # log_file.flush()
    return True


def __check_time(log_time):
    """
    :summary: 校验log_time是否合理
    :param log_time: 201510101000
    :return: boolean
    """
    if len(log_time) != 12:
        return False
    return log_time.isdigit()


def write_to_file(line, topic, log_time, start_time, data_type, postfix=''):
    """
    :summary: 根据传入时间以及日志时间，写入对应文件
    :param line: 需要写入的数据,分为原始日志数据和清洗后的des
    :type line: basestring
    :param topic: kafka－topic名称
    :type topic: basestring
    :param log_time: 需要写入的日志时间,精确到小时
    :type log_time: basestring 201511012200 12位
    :param start_time: 文件后缀名称, 为recv文件的时刻
    :type start_time: basestring 201511012300 12位
    :param data_type: 写入数据的类型，分为 orig,des,des_err,orig_err
    :type data_type: basestring
    :return: boolean 是否成功写入
    """
    if __check_time(log_time):
        return __output_to_files(log_time, line, topic, start_time, data_type, postfix)
    else:
        return False


def close_files():
    for (_k, _v) in file_list.items():
        _v.close()


if __name__ == "__main__":
    pass
