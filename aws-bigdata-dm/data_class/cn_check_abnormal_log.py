# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
from commonlib.common import is_internal_ip
from commonlib.global_var import global_var_client
from datetime import datetime, timedelta
import sys
import string


class CnCheckAbnormalLog(MediaBaseTable):
    """
    :异常流量标记
    """

    def __init__(self, abnormal_time):
        super(CnCheckAbnormalLog, self).__init__()
        self.did_city_map = {}
        self.did_frequency_map = {}
        self.ip_frequency_map = {}

        # 3表示内网ip 直接校验
        self.type_dict = {
            "1": self.did_frequency_map,
            "2": self.did_city_map,
            "4": self.ip_frequency_map
        }

        self.__load_blacklist_map(abnormal_time)

    def __load_blacklist_map(self, abnormal_time):
        """
        加载媒资信息. {file_name: [vid,pid,cid,is_full,duration]}
        :return:
        """
        if len(self.did_city_map) == 0 and len(self.did_frequency_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("abnormal_list", abnormal_time)
            if file_path == "":
                sys.stderr.write("abnormal_file_path is null")
                return
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 7:
                    (e_type, bid, did, begin_time, end_time) = record[0:5]
                    ip_str = record[6]

                    if str(e_type) in self.type_dict:
                        dict_type_map = self.type_dict[str(e_type)]

                        if str(e_type) == "4":
                            key_tmp = ip_str
                        else:
                            key_tmp = did

                        if not isinstance(dict_type_map, dict):
                            sys.stderr.write("abnormal type dict error")
                            sys.exit(-1)

                        if str(key_tmp) == "":
                            continue

                        key = "|".join([str(bid), str(key_tmp)])

                        if key not in dict_type_map:
                            dict_type_map[key] = []

                        dict_type_map[key].append([begin_time, end_time])
                    else:
                        continue
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    @staticmethod
    def is_in_list(time, times_list):
        if not isinstance(times_list, list):
            return False

        for time_info in times_list:
            if len(time_info) != 2:
                continue
            else:
                if str(time_info[0]).isdigit() and str(time_info[1]).isdigit():
                    if int(time_info[0]) <= int(time) <= int(time_info[1]):
                        return True
        return False

    def check_did_frequency(self, input_list):
        """
        检测日志中该用户是否频次异常
        :param input_list: [did,bid,time]
        :return:
        """
        if not isinstance(input_list, list) or len(input_list) != 3:
            return [1, "FORMAT_INPUT_ERR"]

        str_did = str(input_list[0])
        str_bid = str(input_list[1])
        str_time = str(input_list[2])

        if str_did == "" or str_bid == "" or str_did == "-" or str_bid == "-":
            return [1, "DID_OR_BID_NULL"]

        if not str_time.isdigit() or len(str_time) != 14:
            return [1, "TIME_IS_ERR"]

        key = "|".join([str_bid, str_did])

        time_list = self.did_frequency_map.get(key)

        if time_list is None:
            return [0, "0"]
        else:
            if self.is_in_list(str_time, time_list):
                return [0, "1"]
            else:
                return [0, "0"]

    def check_ip_frequency(self, input_list):
        """
        检测日志中该ip是否频次异常
        :param input_list: [ip,bid,time]
        :return:
        """
        if not isinstance(input_list, list) or len(input_list) != 3:
            return [1, "FORMAT_INPUT_ERR"]

        str_ip = str(input_list[0])
        str_bid = str(input_list[1])
        str_time = str(input_list[2])

        if str_ip == "" or str_bid == "" or str_ip == "-" or str_bid == "-":
            return [1, "DID_OR_BID_NULL"]

        if not str_time.isdigit() or len(str_time) != 14:
            return [1, "TIME_IS_ERR"]

        key = "|".join([str_bid, str_ip])

        time_list = self.ip_frequency_map.get(key)

        if time_list is None:
            return [0, "0"]
        else:
            if self.is_in_list(str_time, time_list):
                return [0, "4"]
            else:
                return [0, "0"]

    def check_did_city(self, input_list):
        """
        检测日志中该用户所在城市数是否异常
        :param input_list: [did,bid,time]
        :return:
        """
        if not isinstance(input_list, list) or len(input_list) != 3:
            return [1, "FORMAT_INPUT_ERR"]

        str_did = str(input_list[0])
        str_bid = str(input_list[1])
        str_time = str(input_list[2])

        if str_did == "" or str_bid == "" or str_did == "-" or str_bid == "-":
            return [1, "DID_OR_BID_NULL"]

        if not str_time.isdigit() or len(str_time) != 14:
            return [1, "TIME_IS_ERR"]

        key = "|".join([str_bid, str_did])

        time_list = self.did_city_map.get(key)

        if time_list is None:
            return [0, "0"]
        else:
            if self.is_in_list(str_time, time_list):
                return [0, "2"]
            else:
                return [0, "0"]

    def check_internal_ip(self, ip_list):
        """
        检测ip是否是私网ip
        :param ip_list:
        :return:
        """
        if not isinstance(ip_list, list) or len(ip_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        str_ip = str(ip_list[0])

        if str_ip == "" or str_ip == "-":
            return [1, "INPUT_IS_NULL"]

        if str_ip == "127.0.0.1" or is_internal_ip(str_ip):
            return [0, "3"]
        else:
            return [0, "0"]

process_time = global_var_client.get_global_process_time()
if process_time == "" and len(process_time) != 10:
    sys.stderr.write("input process time error!")
    sys.exit(-1)

try:
    time_time = datetime.strptime(process_time, "%Y%m%d%H")
    time_tmp = time_time + timedelta(hours=1)
    time_str = time_tmp.strftime("%Y%m%d%H")
except (ValueError, TypeError):
    sys.stderr.write("input process time value error!")
    sys.exit(-1)

cn_check_abnormal_log_client = CnCheckAbnormalLog(time_str)