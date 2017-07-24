# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-18T18:59:26+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T19:54:25+08:00
from rule.rule import rule
import re


class cn_refsitetype(rule):
    '''
    :
    '''


    def __init__(self):
        self.regex = "^(http|https)://([0-z]+.)?(baidu|youdao|sogou|google|so|m.sm.cn|cn.bing|soku).com"
        self.pattern = re.compile(self.regex)
        self.regex_zn = "^(http|https)://([0-z]+.)?(mgtv|hunantv|imgo).(com|tv)"
        self.pattern_zn = re.compile(self.regex_zn)


    def convert(self, fields):
        '''
        :
        '''
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            ref_str = fields[0].strip()
            if ref_str == "" or ref_str == "-":
                return [0, 3]

            match = self.pattern.match(ref_str)
            if not match:
                match_zn = self.pattern_zn.match(ref_str)
                if not match_zn:
                    if "http" in ref_str:
                        return [0, 2]
                    else:
                        return [0, 3]
                else:
                    return [0, 4]
            else:
                return [0, 1]
