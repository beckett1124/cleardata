#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T20:04:06+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T21:26:37+08:00
from rule.rule import rule


class com_time_hour(rule):
    '''
    :根据DATE获取小时
    '''


    def __init__(self):
        super(com_time_hour, self).__init__()


    def convert(self,fields):
        '''
        :获取小时 从TIME里面获取
        '''
        if len(fields)!=1 and len(fields[0])>=6:
            return [1,"input_error"]
        else:
            return [0,fields[0][0:2]]
