#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T17:15:00+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:13:56+08:00

import re
import urllib

from rule.rule import rule
from rule.dict_page.dict_mobile_page import mobile_page
from rule.dict_page.dict_mobile_page import mobile_H5_pron_regex
from rule.dict_page.dict_mobile_page import mobile_pron_type


class cn_mobile_pron(rule):
    '''
    :Mobile REF
    '''

    def __init__(self):
        pass

    def convert(self, fields):
        '''
        :Mobile ref_pron转换类，FPN FPID 根据版本做对应的规则
        '''
        #FPN FPID为空
        if len(fields) < 2:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "":
                return [1, "CPN_IS_NULL"]
            else:
                # 当cpn＝1 cpid=62 时，表示轮播/直播产品线 直接返回
                if str(fields[0]) == "1" and (str(fields[1]) == "62" or str(fields[1]) == "1011"):
                    return [0, 1000079]

                # 当cpn＝1 cpid=68 时，表示会员产品线 直接返回
                if str(fields[0]) == "1" and (str(fields[1]) == "68" or str(fields[1]) == "1024"):
                    return [0, 1000075]

                pron_type = mobile_pron_type.get(str(fields[0]))

                # 56 特殊产品线
                if pron_type is not None and pron_type == "url_regex":
                    match_flag = False
                    for (key, value) in mobile_H5_pron_regex.items():
                        for regex in value:
                            pattern = re.compile(regex[0])
                            url_str = urllib.unquote(str(fields[1])).strip()
                            match = pattern.match(url_str)

                            if not match:
                                continue

                            match_flag = True
                            break

                        if match_flag:
                            return [0, key]

                com_page = mobile_page

                _page_type_list = com_page.get(str(fields[0]))
                if _page_type_list is None or len(_page_type_list) < 2:
                    return [0, "-1"]
                else:
                    return [0, _page_type_list[1]]