#encoding: utf-8
# @Author: gibbs
# @Date:   2016-09-08
# @Last modified by:   gibbs
# @Last modified time: 2016-09-08
from rule.rule import rule
from data_class.cn_ip_region import cn_ip_region_client


class cn_check_domestic_by_ip(rule):
    """
    :是否国内
    """

    def __init__(self):
        self.list_domestic = ['香港新世界电讯骨干网', '中国']

    def convert(self, fields):
        """
        :根据IP判断是否国内
        :return [err_no, is_domestic], is_domestic为0，表示国内
        """
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            _res = cn_ip_region_client.get_country_by_ip(fields)

            if _res[0] != 0:
                return _res

            if _res[1].strip() in self.list_domestic:
                return [0, 0]
            else:
                return [0, 1]
