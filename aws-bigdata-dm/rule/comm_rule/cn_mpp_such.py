# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.cn_mpp_channel import cn_mpp_channel_client


class CnMppSubCh(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnMppSubCh, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        return cn_mpp_channel_client.get_sub_ch_by_source(field, 2)

