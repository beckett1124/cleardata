#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T14:20:17+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T15:28:03+08:00
from rule.rule import rule


class cn_fix_vv_cpn(rule):
    '''
    :cpn 字段映射
    '''

    def __init__(self):
        pass

    def convert(self, cpn):
        '''
        :根据 clienttp输出BID字段
        '''
        if len(cpn) != 1:
            return [1, "input_error"]

        if str(cpn[0]) == "81":
            return [0, 6]
        elif str(cpn[0]) == "83":
            return [0, 5]
        elif str(cpn[0]).isdigit() and str(cpn[0]) != "0":
            return [0, cpn[0]]
        else:
            return [0, "\N"]
