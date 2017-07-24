#encoding: utf-8
# @Author: gibbs
# @Date:   2016-09-08
# @Last modified by:   gibbs
# @Last modified time: 2016-09-08
from rule.rule import rule


class cn_ott_check_5(rule):
    """
    :是否国内
    """

    def __init__(self):
        pass

    def convert(self, fields):
        """
        :根据版本号是否国内
        :return [err_no, is_domestic], is_domestic为0，表示国内
        """
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "－":
                return [1, "version_is_null"]
            else:
                if str(fields[0]).lower().startswith("5."):
                    return [0, 0]
                else:
                    return [0, 1]
