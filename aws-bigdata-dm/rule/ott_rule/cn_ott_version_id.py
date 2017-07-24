# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.cn_ott_version import cn_ott_ver_client


class CnOttVersionId(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnOttVersionId, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: vid
        """
        return cn_ott_ver_client.get_ver_id_by_version(field)

