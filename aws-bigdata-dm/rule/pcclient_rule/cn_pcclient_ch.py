# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.cn_mpp_channel import cn_mpp_channel_client


class CnPcClientCh(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnPcClientCh, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        source_list = []

        if not isinstance(field, list) or len(field) != 2:
            return [1, "INPUT_FILED_ERR"]

        source = str(field[0]).lower()

        source_list.append(source)
        source_list.append(field[1])
        return cn_mpp_channel_client.get_ch_by_source(source_list, 1)

