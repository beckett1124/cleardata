#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T09:16:52+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:07:11+08:00
from rule.rule import rule
from rule.ip_rule.cn_city import cn_city
from data_class.cn_ip_region import cn_ip_region_client

class cn_city_by_ip(rule):
    '''
    :换算市列表
    '''

    def __init__(self):
        pass

    def convert(self,fields):
        '''
        :根据名称换算ID
        '''
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            _res = cn_ip_region_client.get_city_by_ip(fields)
            if _res[0] != 0:
                return _res
            return cn_city().convert([_res[1]])
