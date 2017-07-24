#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T14:20:17+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T15:28:03+08:00
from rule.rule import rule


class cn_lower(rule):
    '''
    :换算日志的BID
    '''

    def __init__(self):
        pass

    def convert(self, filed):
        '''
        :转小写
        '''
        if len(filed) < 1:
            return [1, "input_error"]

        if str(filed[0]) != "":
            filed[0] = str(filed[0]).lower().replace("\\x", "")

        return [0, filed[0]]
