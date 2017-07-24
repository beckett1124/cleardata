# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-18T18:59:26+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T19:54:25+08:00
from rule.rule import rule


class cn_url(rule):
    '''
    :url 去掉?后缀
    '''


    def __init__(self):
        pass


    def convert(self, fields):
        '''
        :空值校验
        '''
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            url_str = fields[0]
            # index_ts = url_str.find("?")
            # if index_ts >= 0:
            #     url_str = url_str[0:index_ts]

            return [0, url_str.replace(',', '^').replace('\\', '').replace('\x00', '')[0:1000]]
