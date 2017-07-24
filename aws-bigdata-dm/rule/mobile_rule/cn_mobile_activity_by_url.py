#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T11:00:24+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:02:17+08:00

import re
import urllib
from rule.rule import rule
from data_class.cn_mobile_activity import cn_mobile_activity


class cn_mobile_activity_by_url(rule):
    '''
    :根据URL获取PC WEB类型
    '''

    def __init__(self):
        self.regex_zn = "^(http|https)://([0-z]+.)?(mgtv|hunantv|imgo).(com|tv)"
        self.pattern_zn = re.compile(self.regex_zn)

        self.activity_regex = "^(http|https)://www.(mgtv|hunantv).com/v/(\d{4})/([^/]+)/?"
        self.activity_pattern = re.compile(self.activity_regex)

    def convert(self, fields):
        '''
        :URL 换算
        :1表示站内其他,2站外其他
        '''
        if len(fields) != 2:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "-" or fields[1] == "" or fields[1] == "-":
                return [0, "\N"]
            else:
                page_num = str(fields[0].strip())
                # 非H5页面类直接置空
                if page_num != "56":
                    return [0, fields[1] if str(fields[1]).isdigit() else "\N"]

                url_str = urllib.unquote(fields[1]).strip()

                index_url = url_str.find("?")
                if index_url >= 0:
                    url_str = url_str[0:index_url]

                match_zn = self.pattern_zn.match(url_str)
                if not match_zn:
                    if "http" in url_str:
                        return [0, "2"]
                    else:
                        return [0, "\N"]

                match = self.activity_pattern.match(url_str)
                if not match:
                    return [0, "1"]

                if len(match.groups()) >= 4:
                    activity_url = match.groups()[2] + "/" + match.groups()[3]
                else:
                    return [0, "1"]

                # 调用活动换算id接口
                return cn_mobile_activity.get_activity_id([activity_url])