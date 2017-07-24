#encoding: utf-8
# @Author: tanbo
# @Date:   2016-10-26
# @Last modified by:   tanbo
# @Last modified time: 2016-10-26

from rule.rule import rule
from data_class.cn_ip_region_id import cn_ip_regionid_client


class cn_check_domesticid_by_ip(rule):
    """
    :是否国内
    """

    def __init__(self):
        self.list_domestic = ['10081', '10082', '10083', '10084', '10085', '308', '1']

    def convert(self, fields):
        """
        :根据IP判断是否国内
        :return [err_no, is_domestic], is_domestic为0，表示国内
        """
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            _res = cn_ip_regionid_client.get_country_by_ip(fields)

            if _res[0] != 0:
                return _res

            if _res[1].strip() in self.list_domestic:
                return [0, 0]
            else:
                return [0, 1]
