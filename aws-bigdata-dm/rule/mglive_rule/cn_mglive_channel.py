# encoding: utf-8
# @Author: gibbs
# @Date:   2016-08-10T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-08-10T19:29:22+08:00

from rule.rule import rule
from data_class.mglive_channel_id import mglive_channel_id_client


class CnMgliveChannel(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnMgliveChannel, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(auid)
        :return: id
        """
        return mglive_channel_id_client.get_auto_id_by_channel(field)

