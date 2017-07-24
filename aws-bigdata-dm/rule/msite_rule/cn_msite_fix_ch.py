# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-18T18:59:26+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T19:54:25+08:00
from rule.rule import rule
import urllib


class cn_msite_fix_ch(rule):
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
            try:
                url_str = urllib.unquote(fields[0]).decode('utf8')
            except UnicodeDecodeError:
                try:
                    url_str = urllib.unquote(fields[0]).decode('gbk')
                except UnicodeDecodeError:
                    return [1, "URL_DECODE_ERR"]
            # index_ts = url_str.find("?")
            # if index_ts >= 0:
            #     url_str = url_str[0:index_ts]

            index_url = url_str.find("#")
            if index_url >= 0:
                url_str = url_str[0:index_url]
            return [0, url_str]
