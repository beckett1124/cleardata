#encoding: utf-8
# @Author: gibbs
# @Date:   2016-09-08
# @Last modified by:   gibbs
# @Last modified time: 2016-09-08
from rule.rule import rule
from rule.ip_rule.cn_country import cn_country
from data_class.cn_ip_region import cn_ip_region_client


class cn_country_by_ip(rule):
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
            _res = cn_ip_region_client.get_country_by_ip(fields)
            if _res[0] != 0:
                return _res
            return cn_country().convert([_res[1]])