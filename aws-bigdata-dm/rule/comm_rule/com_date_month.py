#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T10:20:40+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T21:13:28+08:00
from rule.rule import rule

class com_date_month(rule):
    '''
    :获取DATE字段中的的月
    '''

    def __init__(self):
        super(com_date_month, self).__init__()


    def convert(self,date):
        if len(date)!=1 and len(date[0])>=6:
            return [1,"input_error"]
        else:
            return [0,date[0][4:6]]
