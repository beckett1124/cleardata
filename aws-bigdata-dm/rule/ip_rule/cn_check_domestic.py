#encoding: utf-8
# @Author: gibbs
# @Date:   2016-09-08
# @Last modified by:   gibbs
# @Last modified time: 2016-09-08
from rule.rule import rule


class cn_check_domestic(rule):
    """
    :是否国内
    """

    def __init__(self):
        self.list_domestic = ['香港新世界电讯骨干网', '中国']

    def convert(self, fields):
        """
        :根据国家名判断是否国内
        :return [err_no, is_domestic], is_domestic为0，表示国内
        """
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "*":
                return [0, 1]
            else:
                if fields[0].strip() in self.list_domestic:
                    return [0, 0]
                else:
                    return [0, 1]
