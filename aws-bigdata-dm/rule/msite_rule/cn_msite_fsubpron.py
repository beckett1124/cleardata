#encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-19T11:00:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-19T11:02:17+08:00

import re

from rule.rule import rule
from rule.dict_page.dict_msite_page_type import dict_msite_page_type
from rule.dict_page.dist_pcweb_page_type import dist_pcweb_page_type
from rule.dict_page.dict_msite_page_type import msite_pron_type
from rule.dict_page.dist_pcweb_page_type import pcweb_pron_type
from rule.dict_page.dict_msite_page_type import msite_pt_id_map
from rule.dict_page.dist_pcweb_page_type import pcweb_pt_id_map
from rule.dict_page.dict_msite_page_type import dict_msite_page_re_type
from rule.dict_page.dist_pcweb_page_type import dict_pcweb_page_re_type


class cn_msite_fsubpron(rule):
    '''
    :根据URL获取MSITE WEB类型
    '''

    def __init__(self):
        self.regex_zn = "^(http|https)://([0-z]+.)?(beta.)?(mgtv|hunantv|imgo).(com|tv)"
        self.pattern_zn = re.compile(self.regex_zn)
        self.pro_type = ""
        self.dict_page_type = ""
        self.pt_id_map = ""
        self.re_page_type = ""

    def get_m_fsubpron(self, fields):
        if len(fields) < 2:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "-":
                return [0, "-1"]
            else:
                url_str = fields[0].strip()
                match_flag = False

                index_url = url_str.find("?")
                if index_url >= 0:
                    url_str = url_str[0:index_url]

                match_zn = self.pattern_zn.match(url_str)
                if not match_zn:
                    if fields[1] == "phonem":
                        if "http" in url_str:
                            return [0, "-1"]
                        else:
                            return [0, "-1"]
                    else:
                        if "http" in url_str:
                            return [0, "-1"]
                        else:
                            return [0, "-1"]

                pron = ""
                for (key, value) in self.dict_page_type.items():
                    for regex in value:
                        pattern = self.re_page_type[key][regex[0]]
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
                            if fields[1] == "phonem":
                                return [0, "-1"]
                            else:
                                return [0, "-1"]


                # 规则不能匹配的，置为19，表示其他
                if fields[1] == "phonem":
                    return [0, "-1"]
                else:
                    return [0, "-1"]

    def convert(self, fields):
        '''
        :URL 换算
        '''
        if len(fields) < 2:
            return [1, "input_error"]
        else:
            if fields[1] is None or fields[1] == "":
                return [1, "input_error_url"]
            else:
                if fields[1] == "phonem":
                    self.dict_page_type = dict_msite_page_type
                    self.pro_type = msite_pron_type
                    self.pt_id_map = msite_pt_id_map
                    self.re_page_type = dict_msite_page_re_type
                    return self.get_m_fsubpron(fields)
                elif fields[1] == "padweb":
                    self.dict_page_type = dist_pcweb_page_type
                    self.pro_type = pcweb_pron_type
                    self.pt_id_map = pcweb_pt_id_map
                    self.re_page_type = dict_pcweb_page_re_type
                    return [0, "-1"]
