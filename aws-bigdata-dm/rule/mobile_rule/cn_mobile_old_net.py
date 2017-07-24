#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T14:20:17+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T15:28:03+08:00
from rule.rule import rule


class cn_mobile_old_net(rule):
    '''
    :换算日志的BID
    '''

    def __init__(self):
        self.net_map = {
            "none": "0",
            "wifi": "1",
            "3g": "2",
            "4g": "3",
            "2g": "4",
            "cellular": "5"
        }

    def convert(self, net_str):
        '''
        :根据 clienttp输出BID字段
        '''
        if len(net_str) != 1:
            return [1, "input_error"]
        net_low = str(net_str[0]).lower()

        if net_low == "":
            return [0, "\N"]

        _net_id = self.net_map.get(net_low)

        if _net_id is None or _net_id == "":
            return [0, "\N"]
        else:
            return [0, _net_id]
