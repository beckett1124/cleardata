#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T10:21:41+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T11:41:52+08:00
from rule.rule import rule

class com_date_day(rule):
    '''
    :获取DATE字段中的的日
    '''

    def __init__(self):
        super(com_date_day, self).__init__()


    def convert(self,date):
        if len(date)!=1 and len(date[0])>=8:
            return [1,"input_error"]
        else:
            return [0,date[0][6:8]]
