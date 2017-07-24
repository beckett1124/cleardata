#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T11:00:24+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:02:17+08:00

from rule.rule import rule
from rule.pcweb_rule.cn_pcweb_url_protocol import cn_pcweb_url_protocol
from commonlib.common import resolve_url


class cn_mobile_handle_h5_url_protocol(rule):
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

                _res_url = resolve_url(fields[1])

                if _res_url[0] != 0:
                    return _res_url
                else:
                    url_str = _res_url[1]

                return cn_pcweb_url_protocol().convert([url_str])




