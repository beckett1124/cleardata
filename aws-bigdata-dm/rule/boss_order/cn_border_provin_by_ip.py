# encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T09:16:52+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:07:11+08:00

from rule.rule import rule
from data_class.cn_ip_region_id import cn_ip_regionid_client


class cn_border_provinceid_by_ip(rule):
    '''
    :将市份换算成ID
    '''

    def __init__(self):
        pass

    def convert(self,fields):
        '''
        :根据省份名称获取ID
        '''
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            _res = cn_ip_regionid_client.get_province_by_ip(fields)

        if _res[0] != 0:
            return [0, '-1']
        else:
            return _res
