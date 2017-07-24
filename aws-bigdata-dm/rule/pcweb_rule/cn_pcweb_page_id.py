#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T11:00:24+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:02:17+08:00

from rule.rule import rule
from rule.dict_page.dist_pcweb_page_type import dist_pcweb_page_type
from rule.dict_page.dist_pcweb_page_type import dict_pcweb_page_re_type


class cn_pcweb_page_id(rule):
    '''
    :根据URL获取PC WEB类型id
    '''

    def __init__(self):
        pass

    def convert(self, fields):
        '''
        :URL 换算
        '''
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "-":
                return [0, "\N"]
            else:
                url_str = fields[0]

                index_url = url_str.find("?")
                if index_url >= 0:
                    url_str = url_str[0:index_url]

                # 需要换算page_id的页面类型
                page_num_type = ["2", "3"]
                page_id = '\N'
                match_flag = False

                for key in page_num_type:

                    if key not in dist_pcweb_page_type.keys():
                        continue

                    for regex in dist_pcweb_page_type[key]:
                        pattern = dict_pcweb_page_re_type[key][regex[0]]
                        match = pattern.match(url_str)
                        if not match:
                            continue

                        match_flag = True

                        for value in match.groups()[0:2]:
                            if str(value).isdigit():
                                page_id = str(value)
                                break

                        # 匹配成功后,跳出该规则校验
                        break

                    if match_flag:
                        break

                return [0, page_id]