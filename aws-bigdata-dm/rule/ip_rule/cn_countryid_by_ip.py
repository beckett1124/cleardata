#encoding: utf-8
# @Author: tanbo
# @Date:   2016-10-26
# @Last modified by:   tanbo
# @Last modified time: 2016-10-26

from rule.rule import rule
from data_class.cn_ip_region_id import cn_ip_regionid_client


class cn_countryid_by_ip(rule):
    """
    :换算国家列表
    """

    def __init__(self):
        pass

    def convert(self, fields):
        """
        :根据名称换算ID
        """
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            _res = cn_ip_regionid_client.get_country_by_ip(fields)
            return _res