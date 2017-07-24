# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from rule.dict_page.dict_weixin_pagenum import dict_weixin_page_num


class CnWeiXinUrl(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnWeiXinUrl, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(ext1)
        :return: plid
        """

        if not isinstance(field, list) or len(field) < 1:
            return [1, "INPUT_FILED_ERR"]

        url_str = dict_weixin_page_num.get(str(field[0]), '')

        if url_str == "":
            return [0, "未知"]
        else:
            return [0, url_str]

