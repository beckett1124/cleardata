# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.cn_mpp_channel import cn_mpp_channel_client


class CnPcWebSubCh(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnPcWebSubCh, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        source_list = []

        if not isinstance(field, list) or len(field) != 2:
            return [1, "INPUT_FILED_ERR"]

        if field[0] == "":
            return [0, '\N']
        else:
            ref_str = str(field[0]).strip()
            ref_str_list = ref_str.split('/')
            ref_str_list[0] = ''
            source_tmp = '/'.join(ref_str_list[0:3])

        source_list.append(source_tmp + '/')
        source_list.append(field[1])
        return cn_mpp_channel_client.get_sub_ch_by_source(source_list, 2)

