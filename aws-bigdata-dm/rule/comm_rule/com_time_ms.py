#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T16:11:16+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T16:22:53+08:00

from rule.rule import rule

class com_time_ms(rule):
    '''
    :获取分钟加钟数
    '''

    def __init__(self):
        super(com_time_ms, self).__init__()

    def convert(self,mstime):
        '''
        :获从国栋的清洗字段的TIME获取分秒4位数字
        '''
        if len(mstime)!=1 and len(mstime[0])>=4:
            return [1,"input_error"]
        else:
            return [0,mstime[0][2:6]]
