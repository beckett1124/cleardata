#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T11:00:24+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:02:17+08:00

from rule.rule import rule
from rule.mobile_rule.cn_mobile_url_site import cn_mobile_url_site


class cn_mobile_handle_h5_url_site(rule):
    '''
    :根据URL获取PC WEB类型
    '''

    def __init__(self):
        pass

    def convert(self, fields):
        '''
        :URL 换算 CPN CPID
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
                    return [0, "\N"]

                url_str = fields[1]
                
                return cn_mobile_url_site().convert([url_str])




