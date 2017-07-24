#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T11:00:24+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:02:17+08:00

import re

from rule.rule import rule
from rule.dict_page.dist_pcweb_page_type import dist_pcweb_page_type
from rule.dict_page.dist_pcweb_page_type import dict_pcweb_page_re_type


class cn_pcweb_subpron(rule):
    '''
    :根据URL|PT获取PC WEB类型
    '''

    def __init__(self):
        self.regex_zn = "^(http|https)://([0-z]+.)?(mgtv|hunantv|imgo).(com|tv)"
        self.pattern_zn = re.compile(self.regex_zn)

    def convert(self, fields):
        '''
        :URL 换算
        '''
        if len(fields) < 1:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "-":
                return [1, "CPN_IS_NULL"]
            else:
                url_str = fields[0].strip()
                match_flag = False

                index_url = url_str.find("?")
                if index_url >= 0:
                    url_str = url_str[0:index_url]

                match_zn = self.pattern_zn.match(url_str)
                if not match_zn:
                    if "http" in url_str:
                        return [0, "-1"]
                    else:
                        return [0, "-1"]

                pron = ""
                for (key, value) in dist_pcweb_page_type.items():
                    for regex in value:
                        pattern = dict_pcweb_page_re_type[key][regex[0]]
                        match = pattern.match(url_str)
                        if not match:
                            continue

                        match_flag = True

                        if len(regex) > 2:
                            pron = str(regex[2])
                        break

                    if match_flag:
                        if str(pron).isdigit():
                            return [0, pron]
                        else:
                            # 站内其他产品线
                            return [0, "-1"]

                # 规则不能匹配的，置为19，表示其他
                return [0, "-1"]