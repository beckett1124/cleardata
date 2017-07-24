# encoding: utf-8
from rule.rule import rule


class CnFixMobileMf(rule):
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
            filed[0] = str(filed[0]).lower().replace("\\x", "").replace("\x00", "")

        return [0, filed[0]]
