# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
import urllib


class CnFixWebPix(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnFixWebPix, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(pix)
        :return: vid
        """

        if len(field) < 1:
            return [1, "input_error"]

        fix_str = str(urllib.unquote(field[0])).lower()

        if "x" in fix_str:
            fix_str = fix_str.replace('x', '*')

        return [0, fix_str.replace(',', '*')]


