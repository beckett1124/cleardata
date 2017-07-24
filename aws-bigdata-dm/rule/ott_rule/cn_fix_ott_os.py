# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
import urllib
import re


class CnFixOTTOs(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnFixOTTOs, self).__init__()
        self.regex = "^([\d\.]+).*"
        self.pattern = re.compile(self.regex)

    def convert(self, field):
        """
        :param field:  input field data(os)
        :return: vid
        """

        if len(field) < 1:
            return [1, "input_error"]

        os_str = urllib.unquote(str(field[0])).strip()

        if os_str == "" or os_str == "-":
            return [0, "unknown"]

        match = self.pattern.match(str(os_str))

        if match:
            os_str = match.groups()[0]

        return [0, os_str]


