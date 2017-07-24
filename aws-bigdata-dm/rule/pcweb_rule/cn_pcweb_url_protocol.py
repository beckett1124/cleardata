# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-18T18:59:26+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T19:54:25+08:00
from rule.rule import rule


class cn_pcweb_url_protocol(rule):
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

            if url_str is None or url_str == "" or url_str == "-":
                return [0, "\N"]

            url_str = url_str.strip().replace(',', '').replace('\\', '').replace('\x00', '')[0:2046]
            protocol_list  = ["file", "http", "https", "ftp"]
            urlSign = "://"
            for i in protocol_list:
                if url_str.find(i) == 0  and url_str.find(urlSign) > 0 :
                    return  [0, i]

            return [0, "\N"]
