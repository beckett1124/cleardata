#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T18:59:26+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T19:54:25+08:00
from rule.rule import rule

class cn_null(rule):
    '''
    :内容为空校验
    '''


    def __init__(self):
        pass


    def convert(self,fields):
        '''
        :空值校验
        '''
        if len(fields)!=1:
            return [1,"input_error"]
        else:
            if not fields[0] is None and fields[0]=="":
                return [2,"fields_null"]
            else:
                return [0,fields[0]]
