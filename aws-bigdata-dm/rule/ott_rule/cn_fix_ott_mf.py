# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
import urllib


class CnFixOTTMf(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnFixOTTMf, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(mf)
        :return: vid
        """

        if len(field) < 1:
            return [1, "input_error"]

        mf_str = urllib.unquote(str(field[0])).strip().replace("\x00", "").replace(",", "")

        if mf_str == "" or mf_str == "-":
            return [0, "unknown"]

        if "+" in mf_str:
            return [0, mf_str.lower().split('+')[0]]
        else:
            return [0, mf_str.lower().split(' ')[0]]


