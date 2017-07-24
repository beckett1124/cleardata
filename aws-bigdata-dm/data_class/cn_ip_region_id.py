# encoding: utf-8
# @Author: tanbo
# @Date:   2016-10-25T17:06:24+08:00
# @Last modified by:   tanbo
# @Last modified time: 2016-05-17T19:29:22+08:00

import sys
import string
import os
from media_base_table import MediaBaseTable
from commonlib.common import ip_into_int


class CnIpRegionId(object):
    """
    :媒资信息类 CnIpRegionId
    : 0 long_ip_from	 1 long_ip_to  2 country_id	3 province_id	4 city_id	5 isp_id
    """

    def __init__(self):
        self.media_app_cid = {}
        self.GEOIP_SORT = []
        self.GEOIP = {}
        self.loadGeoIp()

    def loadGeoIp(self):
        """
        :summery: 加载ip_region库
        :return: 生成IP_REGION相关DICT
        """
        if len(self.GEOIP) != 0 and len(self.GEOIP_SORT) != 0:
            return

        file_path = MediaBaseTable.get_media_conf_file_name("ip_region")
        if file_path == "":
            sys.stderr.write("get file_path err!")
            sys.exit(-1)

        fp = open(file_path)

        # 跳过第一行
        fp.next()

        for i, line in enumerate(fp):
            try:
                record = string.split(line, "\t")
                rangmin = long(record[0])
                rangmax = long(record[1])
                country = record[2]
                province = record[3]
                city = record[4]
                isp = str(record[5]).strip('\n')

                self.GEOIP[rangmin] = [rangmax, country, province, city, isp]
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
            userip = ip_into_int(userip)
            if userip == 0:
                return None
        except ValueError:
            return None
        location = self._getRangeKey(userip)
        if location and self.GEOIP[location]:
            if location <= userip <= self.GEOIP[location][0]:
                return self.GEOIP[location]
        else:
            return None

    def get_country_by_ip(self, ip_list):
        """
        wash province, 要求log_dict中的time为字符串
        :param ip_list: field name
        :return: [err_num, wash_value or errmsg]
        """
        if not isinstance(ip_list, list) or len(ip_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]
        log_ip = ip_list[0]
        locationtmp = self.formatLocation(log_ip)
        if locationtmp is None or len(locationtmp) <= 2:
            return [1, 'GET_REGION_INFO_ERR']
        return [0, locationtmp[1]]

    def get_province_by_ip(self, ip_list):
        """
        wash province, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if not isinstance(ip_list, list) or len(ip_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]
        log_ip = ip_list[0]
        locationtmp = self.formatLocation(log_ip)
        if locationtmp is None or len(locationtmp) <= 2:
            return [1, 'GET_REGION_INFO_ERR']
        return [0, locationtmp[2]]

    def get_city_by_ip(self, ip_list):
        """
        wash city, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if not isinstance(ip_list, list) or len(ip_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]
        log_ip = ip_list[0]
        locationtmp = self.formatLocation(log_ip)
        if locationtmp is None or len(locationtmp) <= 3:
            return [1, 'GET_REGION_INFO_ERR']
        return [0, locationtmp[3]]

    def get_isp_by_ip(self, ip_list):
        """
        wash 运营商, 要求log_dict中的time为字符串
        :param log_key: field name
        :param log_dict: log dict
        :return: [err_num, wash_value or errmsg]
        """
        if not isinstance(ip_list, list) or len(ip_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]
        log_ip = ip_list[0]

        locationtmp = self.formatLocation(log_ip)
        if locationtmp is None or len(locationtmp) <= 4:
            return [1, 'GET_REGION_INFO_ERR']
        return [0, locationtmp[4]]

cn_ip_regionid_client = CnIpRegionId()
# ip = ["124.232.146.138"]
# ip = ["-12"]
# print cn_ip_regionid_client.get_country_by_ip(ip)
# print cn_ip_regionid_client.get_province_by_ip(ip)
# print cn_ip_regionid_client.get_city_by_ip(ip)
# print cn_ip_regionid_client.get_isp_by_ip(ip)