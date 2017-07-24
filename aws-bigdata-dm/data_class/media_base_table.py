# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from conf.settings import RuleConfig
from commonlib.pydotalog import pydotalog
import sys
import os
from datetime import datetime, timedelta


class MediaBaseTable(object):
    """
    :媒资信息基类
    """

    def __init__(self):
        self.drop_record = 0

    @staticmethod
    def get_media_conf_file_name(table_name, file_time=""):

        time_now = datetime.now()

        is_exists = 0
        file_name = ""

        for i in range(2):
            time_tmp = time_now + timedelta(hours=-i)
            time_str = time_tmp.strftime("%Y%m%d%H")

            if len(file_time) == 10:
                time_str = file_time

            file_name = RuleConfig["Media_table_info"][table_name] % time_str

            if os.path.exists(file_name):
                is_exists = 1
                break

        if is_exists == 1:
            return file_name
        else:
            pydotalog.warning("load conf file failed:%s" % file_name)
            return ""
