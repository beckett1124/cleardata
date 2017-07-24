# encoding: utf-8
# @Author: gibbs
# @Date:   2016-09-08
# @Last modified by:   gibbs
# @Last modified time: 2016-09-08
from rule.rule import rule


class cn_mac_big_ver(rule):
    """
    :是否国内
    """

    def __init__(self):
        pass

    def convert(self, fields):
        """
        :根据版本号换算大小版本
        :return [err_no, ver_msg]
        """
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "－":
                return [1, "version_is_null"]
            else:
                content = str(fields[0])

                _list = content.split('-')
                if len(_list) < 2:
                    return [0, "-1"]

                ver = _list[1].split('.')[0]
                if ver.isdigit():
                    return [0, int(ver)]
                else:
                    return [0, "-1"]
