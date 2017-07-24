# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from rule.dict_page.dict_ott_page_type import ott_page


class cn_ott_page_num(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(cn_ott_page_num, self).__init__()

    def convert(self, field):
        """
        :param field:  input page_num
        :return: cid
        """
        if len(field) == 0:
            return [1, "INPUT_FAILED"]

        _res_page = ott_page.get(field[0])
        if _res_page is None or len(_res_page) <= 1:
            return [0, '\N']
        else:
            return [0, _res_page[1]]