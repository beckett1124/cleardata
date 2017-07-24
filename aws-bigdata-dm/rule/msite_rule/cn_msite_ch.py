# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.cn_mpp_channel import cn_mpp_channel_client
import urllib
from commonlib.common import is_mg_url


class CnMSiteCh(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnMSiteCh, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        source_list = []

        if not isinstance(field, list) or len(field) != 4:
            return [1, "INPUT_FILED_ERR"]

        # if str(field[2]) == "padweb":
        #     return [0, ""]

        source = ""
        if field[0] == "":
            if field[1] != "":
                _source_tmp = str(field[1]).split('_')
                if len(_source_tmp) > 1:
                    source = str(urllib.unquote(_source_tmp[1])).split('?')[0].replace('/', '')
        else:
            source = str(urllib.unquote(field[0])).split('?')[0].replace('/', '')

        if source == "":
            if is_mg_url(field[3]):
                return [0, '']
            else:
                source = "8kpqp21m4cm"

        index_source = source.find("#")
        if index_source >= 0:
            source = source[0:index_source]

        source_list.append(source)
        source_list.append(field[2])
        return cn_mpp_channel_client.get_ch_by_source(source_list, 1)

