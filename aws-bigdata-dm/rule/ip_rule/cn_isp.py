#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T09:16:52+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:07:11+08:00
from rule.rule import rule
from rule.dict_page.dict_isp import dict_isp


class cn_isp(rule):
    '''
    :换算运营商对应id
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
            if fields[0] is None or fields[0] == "" or fields[0] == "*":
                return [0, dict_isp.get("未知")]
            else:
                isp_id = dict_isp.get(fields[0])
                if isp_id is None:
                    return [0, dict_isp.get("未知")]
                else:
                    return [0, isp_id]
