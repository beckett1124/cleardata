# encoding: utf-8
# @Author: gibbs
# @Date:   2016-08-10T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-08-10T19:29:22+08:00

from rule.rule import rule
from data_class.mglive_id_auid import mglive_id_auid_client


class CnMgliveAuid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnMgliveAuid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(auid)
        :return: id
        """
        return mglive_id_auid_client.get_id_by_auid(field)

