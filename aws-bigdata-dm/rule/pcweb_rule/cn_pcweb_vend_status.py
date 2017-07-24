# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

import urllib
from rule.rule import rule
from data_class.cn_mpp_channel import cn_mpp_channel_client


class CnPcWebVendStatus(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnPcWebVendStatus, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        source_list = []

        if not isinstance(field, list) or len(field) != 3:
            return [1, "INPUT_FILED_ERR"]

        if field[0] == "":
            if field[1] == "":
                return [0, '\N']
            else:
                _source_tmp = str(field[1]).split('_')
                if len(_source_tmp) != 2:
                    return [0, '\N']
                source = str(urllib.unquote(_source_tmp[1])).split('?')[0].replace('/', '')
        else:
            source = str(urllib.unquote(field[0])).split('?')[0].replace('/', '')

        source_list.append(source)
        source_list.append(field[2])
        return cn_mpp_channel_client.get_vend_status_by_source(source_list)

